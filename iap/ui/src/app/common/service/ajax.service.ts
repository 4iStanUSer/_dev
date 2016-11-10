import { Injectable } from '@angular/core';
import { Http, Response, Request, RequestMethod, BaseRequestOptions,
    Headers } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import * as _ from 'lodash';
import { LoadingService } from './loading.service';

class ServiceConf {
    //request: RequestConf = new RequestConf('ajax');
}

class ServerResponse {
    error: boolean = false;
    data: Object = {};

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

interface IRequestOptions {
    url: string;
    method?: string; // 'get', 'post', 'put', 'delete', 'head'
    data?: any;
    //headers: Object;
    //content_type: string;
    //...
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
    private serviceConf: ServiceConf = new ServiceConf();
    private counter: number = 0;

    constructor(private http: Http, private loading: LoadingService) { }

    public configure(serv_config: Object = {}) {
        _.extend(this.serviceConf, serv_config);
    }

    public get(options: IRequestOptions) : Observable<Subject<any>> {
        options.method = 'post';
        let req = this._makeRequestInst(options);

        return this._query(req);
    }
    public post(options: IRequestOptions) : Observable<Subject<any>> {
        options.method = 'post';
        let req = this._makeRequestInst(options);

        return this._query(req);
    }

    private _query(req: Request) {
        // TODO Loading Procedure
        let blackBox = <Subject<any>>new Subject();

        this.counter += 1;
        let pid = 'request_' + this.counter;
        this.loading.show(pid);

        let r = this.http.request(req)
            .map((res: Response) => {
                let body = res.json();
                let resp = new ServerResponse();
                _.extend(resp, body);
                return resp;
            });

        // r.subscribe( // TODO check unsubscribe for blackbox subscription
        //     (res: ServerResponse) => {
        //         if (res.hasError()) {
        //             this._handleSiteError(res, blackBox);
        //         } else {
        //             blackBox.next(res.data);
        //         }
        //         this.loading.hide(pid);
        //     },
        //     (err: Response) => {
        //         this.loading.hide(pid);
        //         this._handleServerError(err, blackBox);
        //     }
        // );
        // return r;
        r.subscribe( // TODO check unsubscribe for blackbox subscription
            (res: ServerResponse) => {
                if (res.hasError()) {
                    this._handleSiteError(res, blackBox);
                } else {
                    blackBox.next(res.data);
                }
                this.loading.hide(pid);
            },
            (err: Response) => {
                this.loading.hide(pid);
                this._handleServerError(err, blackBox);
            }
        );
        // return blackBox.asObservable();
        return blackBox;
    }

    private _handleSiteError(res: ServerResponse, blackBox: Subject<any>) {
        // TODO Show error at view
        console.error('App Error message: ' + res.getError());
        //blackBox.error(res.getError()); // TODO Refactor (VL)
    }

    private _handleServerError(error: Response, blackBox: Subject<any>) {
        // TODO handlers for ERROR TYPES
        if (error.status === 500) {
        } else if (error.status === 404) {
        }
        // TODO Show error at view
        console.error('Server Error message: ' + error.status);
        //blackBox.error(error.status); // TODO Refactor (VL)
    }

    private _makeRequestInst(options: IRequestOptions): Request {
        let reqOpt = new BaseRequestOptions();
        let headers = new Headers();

        let obj_for_merge = {};

        if (!options['url']) {
            console.error('Have no url property!');
            return null;
        } else if (!_.isString(options['url']) || !options['url'].length) {
            console.error('Wrong url property!');
            return null;
        }
        obj_for_merge['url'] = options['url'];

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
                obj_for_merge['search'] = this._objectToQueryString(options.data);
            } else {
                console.error('Can\'t procced value!');
            }
        } else {
            console.error('Have no such method!');
        }

        return new Request(reqOpt.merge(obj_for_merge));
    }
    private _objectToQueryString (obj: any) {
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
