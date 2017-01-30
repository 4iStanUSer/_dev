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

/**
 * Any server response wrap by this class.
 * It knows about data logic of server response.
 * It also might to know about request options - TODO Implement this
 */
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

    isAuthError() {
        return this.data === 'auth-error'; // TODO Generate error codes
    }
}

/**
 * Describes input data for one query
 */
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

/**
 * Describes configuration of url into urlsMapper.
 * It is received from backend
 */
type UrlConfig = {
    'url': string;
    'allowNotAuth': boolean;
};

/**
 * Describes item in requests queue.
 */
type QueueItem = {
    id: number;
    url_id: string;
    sync: boolean;
    sent: boolean;
    request: Request;
    observable: Subject<any>
}



@Injectable()
/**
 * AjaxService (service) - object for sending requests to server side.
 * First of all it loads urlMapper from server (before first query).
 * It uses queue of requests. Requests may be 2 types: sync and async.
 * If service meets sync request - other requests wait for resolving
 * this sync request.
 * Main public methods are - .get(), .post()
 * If property allowToRequest equals to true - allow requesting,
 * otherwise - decline requesting.
 * Simply usage inside component/services/etc.:
 *  this.request.get({
 *      url_id: 'forecasting/get_data',
 *      data: {
 *          param: '123',
 *          param2: 456,
 *          param3: [7, 8, 9]
 *      }
 *  })
 *  .subscribe(
 *      (d) => {
 *          this.get_data_ = d;
 *      },
 *      (e) => {
 *          console.log(e);
 *      },
 *      () => {
 *          console.log('Complete!');
 *      }
 *  );
 */
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
    private urlsSource: string = '/routing_config';

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

    /**
     * Link to AuthService
     * @type {AuthService}
     */
    auth: AuthService = null;

    constructor(private http: Http,
                private loading: LoadingService) {
        this.loadUrlMapper();
    }

    /**
     * Add request(QueueItem object) into queue and run this.mapQueue()
     * @param options: IRequestOptions
     * @returns {Observable<any>}
     */
    get(options: IRequestOptions): Observable<any> { //Subject<any>
        // TODO Fix bad request !!!
        console.log('Start get, options', options);
        if (!this.urlsMapper && !this.reqForUrlMapperSent) {
            console.log("Load Url Mapper");
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
            let new_data = {'data': options.data, 'X_Token':localStorage.getItem('currentUser')};
            let req = this.makeRequestInst({
                url: this.getUrl(url_id),
                method: 'get',
                data: new_data
            });
            console.log('reqQueue',req);
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
            }, 25);
            return subject;
        } else {
            console.error('Wrong request "url_id" property')
        }
        return null;
    }

    post(options: IRequestOptions): Observable<any> {
        // TODO Fix bad request !!!
        console.log('Start post, options', options);
        if (!this.urlsMapper && !this.reqForUrlMapperSent) {
            console.log("Load Url Mapper");
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
            let new_data = {'data': options.data, 'X-Token':localStorage.getItem('currentUser')};
            let req = this.makeRequestInst({
                url: this.getUrl(url_id),
                method: 'post',
                data: new_data

            });
            console.log('reqQueue',req);
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
            }, 25);
            console.log('Subject', subject);
            return subject;
        } else {
            console.error('Wrong request "url_id" property')
            return null;
        }
    }

    /**
     * Sorts out queue of requests and run this.startQuery() for each item if:
     * - allow to request (this.allowToRequest == true)
     * - current request was not sent
     * If found synchronous request - sends request and breaks the loop
     */
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

    /**
     * Sends query to server for passed QueueItem;
     * Subscribes for resolving query and run .next() method
     * on QueueItem's observable - for execution subscribers of
     * external components/services/etc.
     * After execution all external subscribers - run this.endQuery()
     * @param item
     */
    private startQuery(item: QueueItem) {
        if (item.sync) {
            this.allowToRequest = false;
        }
        item.sent = true;
        if (!item.request.url && item.url_id) {
            item.request.url = this.getUrl(item.url_id);
        }
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

    /**
     * Removes passed QueueItem from queue of requests
     * and if found - run sort out the queue
     * @param item
     */
    private endQuery(item: QueueItem) {
        for (let i = 0; i < this.reqQueue.length; i++) {
            if (item.id == this.reqQueue[i].id) {
                this.reqQueue.splice(i, 1);
                this.mapQueue();
                break;
            }
        }
    }

    /**
     * Loads urls and info for each of them from server.
     * Must be executed before first query.
     * If it not executed - AjaxService doesn't know where to send queries.
     * It adds synchronous query into queue.
     */
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

    /**
     * Low-level method for execution any query to server.
     * Should be used only by members of AjaxService.
     * If it receives error from server (server error or application error) -
     * runs private methods for handling this error.
     * It uses LoadingService inside.
     * Returns Observable 'BlackBox', which will be resolved
     * when server answers for query.
     * @param req Request
     * @returns {Subject<any>}
     */
    private query(req: Request): Subject<any> {
        // TODO REMAKE - delete blackBox
        let blackBox = new Subject<any>();

        this.counter += 1;
        let pid = 'request_' + this.counter;
        this.loading.show(pid);
        console.log('HTTP Request',req);

        this.http.request(req)
            .map((res: Response) => {

                let body = res.json();
                let resp = new ServerResponse();
                _.extend(resp, body);
                // TODO Add request meta into Response
                console.log(resp);
                console.log(body);
                return resp;
            }).subscribe( // TODO check unsubscribe for blackbox subscription
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

    /**
     * Handles application error and runs .error() method on query 'BlackBox'.
     * If this error is auth error - runs this.auth.logoutByBackend()
     * @param res
     * @param blackBox
     */
    private handleSiteError(res: ServerResponse, blackBox: Subject<any>) {
        // TODO Show error at view
        console.log(res)

        if (res.isAuthError() && this.auth) {
            console.log("App data:" + res.getData());
            this.auth.logoutByBackend();
            console.error('App Error message: ' + res.getError());
            // TODO Implement procedure of route reload when ajax request has auth error
        }
        else {
            blackBox.error(res.getError());
        }
    }

    /**
     * Handles specific errors - server errors.
     * Runs error callback on higher subscribers.
     * @param error
     * @param blackBox
     */
    private handleServerError(error: Response, blackBox: Subject<any>) {
        // TODO handlers for ERROR TYPES
        console.log(error);
        if (error.status === 500) {
        } else if (error.status === 404) {
        }
        // TODO Show error at view
        console.error('Server Error message: ' + error.status);
        blackBox.error(error.status);
    }

    /**
     * Returns string url for url_id. Source of urls - this.urlsMapper.
     * If can't get url path - returns null.
     * @param url_id
     * @returns {String}
     */
    private getUrl(url_id: string) {
        return url_id;
        //return (url_id && this.urlsMapper && this.urlsMapper[url_id])
        //    ? this.urlsMapper[url_id].url : null;
    }

    /**
     * Low-level method for creating Request object for Angular Http Service.
     * Creates request object with body in JSON format.
     * Default request method = POST
     * @param options {url: string, method: string, data: any}
     * @returns {Request}
     */
    private makeRequestInst(options: {
        url: string;
        method: string;
        data: any;
    }): Request {

        let reqOpt = new BaseRequestOptions();
        let headers = new Headers();
        let obj_for_merge = {
            'url': options['url']
        };

        let method = RequestMethod.Post;
        console.log('Request Method', options.method);
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

    /**
     * Transforms input variable in safe query string.
     * It uses encodeURIComponent() method.
     * It doesn't include variable into result structure if value
     * equals null or undefined!
     * @param obj
     * @returns {string}
     */
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
