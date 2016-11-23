import {Injectable} from '@angular/core';
import {
    Http, Response, Request, RequestMethod, BaseRequestOptions,
    Headers
} from '@angular/http';
import {Observable} from 'rxjs/Observable';
import {Subject} from 'rxjs/Subject';
import * as _ from 'lodash';
import {LoadingService} from './loading.service';
import {AuthService} from "./auth.service";

class ServiceConf {
    //request: RequestConf = new RequestConf('ajax');
}

class ServerResponse {
    error: boolean = false;
    data: Object = {};
    request: Object = {};

    hasError() {
        return !!this.error;
    }

    getError() {
        return this.data;
    }

    getData() {
        return this.data;
    }
}


interface IRequestOptions { // TODO Separate outside and inside interfaces
    url_id: string;
    method?: string; // 'get', 'post', 'put', 'delete', 'head'
    data?: any;
    url?: string;
    sync?: boolean;
    //headers: Object;
    //content_type: string;
    //...
}

type UrlConfig = {
    'url': string;
    'allowNotAuth': boolean;
};
type QueueItem = {
    id: number;
    url_id: string;
    sync: boolean;
    sent: boolean;
    request: Request;
    observable: Subject<any>
}

/**
 * Using:
 * this.request
 .get({
                url: '/forecasting/get_data',
                data: {
                    param: '123',
                    param2: 456,
                    param3: [7, 8, 9]
                }
            })
 .subscribe(
 (d) => {
                    this.get_data_ = d;
                },
 (e) => {
                    console.log(e);
                },
 () => {
                    console.log('Complete!');
                }
 );
 */
@Injectable()
export class AjaxService {
    /**
     * Shows ability to do request in this moment
     * @type {boolean}
     */
    private allowToRequest: boolean = true;

    /**
     * Url for getting urls configuration
     * @type {string}
     */
    private urlsSource: string = '/temp/get_urls';

    /**
     * Flag for request for urlMapper
     * @type {boolean}
     */
    private reqForUrlMapperSent: boolean = false;

    /**
     * Contains urls configuration
     * @type {{[url_id: string]: UrlConfig}}
     */
    private urlsMapper: {
        [url_id: string]: UrlConfig
    } = null;

    /**
     * Contains queue of requests
     * @type {Array<QueueItem>}
     */
    private reqQueue: Array<QueueItem> = [];

    /**
     * Counter for generating unique process ID
     * @type {number}
     */
    private counter: number = 0;

    // private serviceConf: ServiceConf = new ServiceConf();

    constructor(private http: Http,
                private loading: LoadingService,
                private auth: AuthService) {

        // this.urlsMapper = urlConf; // TODO Remove & remake
    }

    // public configure(serv_config: Object = {}) {
    //     _.extend(this.serviceConf, serv_config);
    // }

    /**
     * Add request(QueueItem object) into queue and run this.mapQueue()
     * @param options: IRequestOptions
     * @returns {Observable<any>}
     */
    get(options: IRequestOptions): Observable<any> { //Subject<any>
        // TODO Fix bad request !!!
        if (!this.urlsMapper && !this.reqForUrlMapperSent) {
            this.loadUrlMapper();
        }
        if (
            options.url_id
            && typeof options.url_id == 'string'
            && options.url_id.length > 0
        ) {
            let id = this.counter++;
            let sync = (options.sync) ? options.sync : false;
            let url_id = options.url_id;
            let subject = new Subject<any>();
            let req = this.makeRequestInst({
                url: this.getUrl(url_id),
                method: 'post',
                data: options.data
            });
            this.reqQueue.push({
                'id': id,
                'url_id': url_id,
                'sync': sync,
                'sent': false,
                'observable': subject,
                'request': req
            });
            // subject.subscribe((data) => {
            //     console.log('subject.subscribe', data);
            // });
            setTimeout(() => {
                this.mapQueue(); // TODO Review
            }, 10);
            return subject;
        } else {
            console.error('Wrong request "url_id" property')
        }
        return null;
    }

    post(options: IRequestOptions): Observable<any> {
        console.error('Implement AjaxService.post()');
        return null;
    }

    private mapQueue() {
        if (!this.allowToRequest) return;

        for (let i = 0; i < this.reqQueue.length; i++) {
            if (this.reqQueue[i].sent) continue;

            if (this.reqQueue[i].sync) {
                this.startQuery(this.reqQueue[i]);
                break;
            } else {
                this.startQuery(this.reqQueue[i]);
            }
        }
    }

    private startQuery(item: QueueItem) {
        if (item.sync) {
            this.allowToRequest = false;
        }
        item.sent = true;
        if (!item.request.url && item.url_id) {
            item.request.url = this.getUrl(item.url_id);
        }
        // console.log(item.request.url);
        if (item.request.url) {
            this.query(item.request).subscribe((data) => {
                    if (item.sync) {
                        this.allowToRequest = true;
                    }
                    item.observable.next(data);
                    this.endQuery(item);
                },
                (e) => {
                    if (item.sync) {
                        this.allowToRequest = true;
                    }
                    item.observable.error(e);
                    this.endQuery(item);
                }); // TODO Check this and add complete method
        } else {
            console.error('Didn\'t receive url(s) for AjaxService.urlMapper');
            item.observable.error(null);
        }
    }

    private endQuery(item: QueueItem) {
        for (let i = 0; i < this.reqQueue.length; i++) {
            if (item.id == this.reqQueue[i].id) {
                this.reqQueue.splice(i, 1);
                this.mapQueue();
                break;
            }
        }
    }

    private loadUrlMapper() {
        this.reqForUrlMapperSent = true;
        let subject = new Subject<any>();
        this.reqQueue.push({
            'id': this.counter++,
            'url_id': null,
            'sync': true,
            'sent': false,
            'observable': subject,
            'request': this.makeRequestInst({
                url: this.urlsSource,
                method: 'post',
                data: {}
            })
        });
        subject.subscribe((data) => {
            console.info('-->AjaxService->Received urlsMapper');
            this.urlsMapper = data;
        });
        setTimeout(() => {
            this.mapQueue();
        }, 10);
    }

    private query(req: Request): Subject<any> {
        // TODO REMAKE - delete blackBox
        let blackBox = new Subject<any>();

        this.counter += 1;
        let pid = 'request_' + this.counter;
        this.loading.show(pid);

        this.http.request(req)
            .map((res: Response) => {
                let body = res.json();
                let resp = new ServerResponse();
                _.extend(resp, body);
                // TODO Add request meta into Response
                return resp;
            })
            .subscribe( // TODO check unsubscribe for blackbox subscription
                (res: ServerResponse) => {
                    this.loading.hide(pid);
                    if (res.hasError()) {
                        this.handleSiteError(res, blackBox);
                    } else {
                        blackBox.next(res.data);
                    }
                },
                (err: Response) => {
                    this.loading.hide(pid);
                    this.handleServerError(err, blackBox);
                }
            );
        return blackBox;
    }

    private handleSiteError(res: ServerResponse, blackBox: Subject<any>) {
        // TODO Show error at view
        console.error('App Error message: ' + res.getError());
        blackBox.error(res.getError()); // TODO Refactor (VL)
    }

    private handleServerError(error: Response, blackBox: Subject<any>) {
        // TODO handlers for ERROR TYPES
        if (error.status === 500) {
        } else if (error.status === 404) {
        }
        // TODO Show error at view
        console.error('Server Error message: ' + error.status);
        blackBox.error(error.status); // TODO Refactor (VL)
    }

    private getUrl(url_id: string) {
        return (url_id && this.urlsMapper && this.urlsMapper[url_id])
            ? this.urlsMapper[url_id].url : null;
    }

    private makeRequestInst(options: {
        url: string;
        method: string;
        data: any;
    }): Request { //IRequestOptions
        // if (typeof options['url'] != 'string' || options['url'].length == 0) {
        //     console.error('Wrong url_id property!');
        //     return null;
        // } // TODO Review maybe this is not needed

        let reqOpt = new BaseRequestOptions();
        let headers = new Headers();
        let obj_for_merge = {
            'url': options['url']
        };

        let method = RequestMethod.Post;
        if (options.method && options.method != 'post') {
            switch (options.method) {
                case 'get':
                    method = RequestMethod.Get;
                    break;
                case 'put':
                    method = RequestMethod.Put;
                    break;
                case 'delete':
                    method = RequestMethod.Delete;
                    break;
                case 'head':
                    method = RequestMethod.Head;
                    break;
            }
        }
        obj_for_merge['method'] = method;

        if (method === RequestMethod.Post) {
            // obj_for_merge['body'] = {
            //     'params': options.data
            // }; //let body = JSON.stringify({ name });

            obj_for_merge['body'] = JSON.stringify(options.data);

            headers.append('Content-Type', 'application/json;charset=UTF-8');
            obj_for_merge['headers'] = headers;
        } else if (method === RequestMethod.Get) {
            if (_.isString(options.data)) {
                obj_for_merge['search'] = options.data;
            } else if (_.isObject(options.data)) {
                obj_for_merge['search'] = this.objectToQueryString(options.data);
            } else {
                console.error('Can\'t procced value!');
            }
        } else {
            console.error('Have no such method!');
        }

        return new Request(reqOpt.merge(obj_for_merge));
    }

    private objectToQueryString(obj: any) {
        var qs = _.reduce(obj, function (result, value, key) {
            if (!_.isNull(value) && !_.isUndefined(value)) {
                if (_.isArray(value)) {
                    result += _.reduce(value, function (result1, value1) {
                        if (!_.isNull(value1) && !_.isUndefined(value1)) {
                            result1 += key + '=' + value1 + '&';
                            return result1
                        } else {
                            return result1;
                        }
                    }, '')
                } else {
                    result += encodeURIComponent(key.toString()) + '=' +
                        encodeURIComponent(value.toString()) + '&';
                }
                return result;
            } else {
                return result
            }
        }, '').slice(0, -1);
        return qs;
    };
}
