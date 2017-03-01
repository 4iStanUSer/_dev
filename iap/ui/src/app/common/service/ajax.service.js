"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var core_1 = require('@angular/core');
var http_1 = require('@angular/http');
var Subject_1 = require('rxjs/Subject');
var _ = require('lodash');
/**
 * Any server response wrap by this class.
 * It knows about data logic of server response.
 * It also might to know about request options - TODO Implement this
 */
var ServerResponse = (function () {
    function ServerResponse() {
        this.error = false;
        this.data = {};
        this.request = {};
    }
    ServerResponse.prototype.hasError = function () {
        return !!this.error;
    };
    ServerResponse.prototype.getError = function () {
        return this.data;
    };
    ServerResponse.prototype.getData = function () {
        return this.data;
    };
    ServerResponse.prototype.isAuthError = function () {
        return this.data === 'auth-error'; // TODO Generate error codes
    };
    return ServerResponse;
}());
var AjaxService = (function () {
    function AjaxService(http, loading) {
        this.http = http;
        this.loading = loading;
        /**
         * Shows ability to do request in this moment
         * @type {boolean}
         */
        this.allowToRequest = true;
        /**
         * Url for getting urls configuration
         * @type {string}
         */
        this.urlsSource = '/routing_config';
        /**
         * Flag for request for urlMapper
         * @type {boolean}
         */
        this.reqForUrlMapperSent = false;
        /**
         * Contains urls configuration
         * @type {{[url_id: string]: UrlConfig}}
         */
        this.urlsMapper = null;
        /**
         * Contains queue of requests
         * @type {Array<QueueItem>}
         */
        this.reqQueue = [];
        /**
         * Counter for generating unique process ID
         * @type {number}
         */
        this.counter = 0;
        /**
         * Link to AuthService
         * @type {AuthService}
         */
        this.auth = null;
        this.loadUrlMapper();
    }
    /**
     * Add request(QueueItem object) into queue and run this.mapQueue()
     * @param options: IRequestOptions
     * @returns {Observable<any>}
     */
    AjaxService.prototype.get = function (options) {
        var _this = this;
        // TODO Fix bad request !!!
        console.log('Start get, options', options);
        if (!this.urlsMapper && !this.reqForUrlMapperSent) {
            console.log("Load Url Mapper");
            this.loadUrlMapper();
        }
        if (options.url_id
            && typeof options.url_id == 'string'
            && options.url_id.length > 0) {
            var id = this.counter++;
            var sync = (options.sync) ? options.sync : false;
            var url_id = options.url_id;
            var subject = new Subject_1.Subject();
            var new_data = { 'data': options.data, 'X_Token': localStorage.getItem('currentUser') };
            var req = this.makeRequestInst({
                url: this.getUrl(url_id),
                method: 'get',
                data: new_data
            });
            console.log('reqQueue', req);
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
            setTimeout(function () {
                _this.mapQueue(); // TODO Review
            }, 25);
            return subject;
        }
        else {
            console.error('Wrong request "url_id" property');
        }
        return null;
    };
    AjaxService.prototype.post = function (options) {
        var _this = this;
        // TODO Fix bad request !!!
        console.log('Start post, options', options);
        if (!this.urlsMapper && !this.reqForUrlMapperSent) {
            console.log("Load Url Mapper");
            this.loadUrlMapper();
        }
        if (options.url_id
            && typeof options.url_id == 'string'
            && options.url_id.length > 0) {
            var id = this.counter++;
            var sync = (options.sync) ? options.sync : false;
            var url_id = options.url_id;
            var subject = new Subject_1.Subject();
            var new_data = { 'data': options.data, 'X-Token': localStorage.getItem('currentUser') };
            var req = this.makeRequestInst({
                url: this.getUrl(url_id),
                method: 'post',
                data: new_data
            });
            console.log('reqQueue', req);
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
            setTimeout(function () {
                _this.mapQueue(); // TODO Review
            }, 25);
            console.log('Subject', subject);
            return subject;
        }
        else {
            console.error('Wrong request "url_id" property');
            return null;
        }
    };
    /**
     * Sorts out queue of requests and run this.startQuery() for each item if:
     * - allow to request (this.allowToRequest == true)
     * - current request was not sent
     * If found synchronous request - sends request and breaks the loop
     */
    AjaxService.prototype.mapQueue = function () {
        if (!this.allowToRequest)
            return;
        for (var i = 0; i < this.reqQueue.length; i++) {
            if (this.reqQueue[i].sent)
                continue;
            if (this.reqQueue[i].sync) {
                this.startQuery(this.reqQueue[i]);
                break;
            }
            else {
                this.startQuery(this.reqQueue[i]);
            }
        }
    };
    /**
     * Sends query to server for passed QueueItem;
     * Subscribes for resolving query and run .next() method
     * on QueueItem's observable - for execution subscribers of
     * external components/services/etc.
     * After execution all external subscribers - run this.endQuery()
     * @param item
     */
    AjaxService.prototype.startQuery = function (item) {
        var _this = this;
        if (item.sync) {
            this.allowToRequest = false;
        }
        item.sent = true;
        if (!item.request.url && item.url_id) {
            item.request.url = this.getUrl(item.url_id);
        }
        if (item.request.url) {
            this.query(item.request).subscribe(function (data) {
                if (item.sync) {
                    _this.allowToRequest = true;
                }
                item.observable.next(data);
                _this.endQuery(item);
            }, function (e) {
                if (item.sync) {
                    _this.allowToRequest = true;
                }
                item.observable.error(e);
                _this.endQuery(item);
            }); // TODO Check this and add complete method
        }
        else {
            console.error('Didn\'t receive url(s) for AjaxService.urlMapper');
            item.observable.error(null);
        }
    };
    /**
     * Removes passed QueueItem from queue of requests
     * and if found - run sort out the queue
     * @param item
     */
    AjaxService.prototype.endQuery = function (item) {
        for (var i = 0; i < this.reqQueue.length; i++) {
            if (item.id == this.reqQueue[i].id) {
                this.reqQueue.splice(i, 1);
                this.mapQueue();
                break;
            }
        }
    };
    /**
     * Loads urls and info for each of them from server.
     * Must be executed before first query.
     * If it not executed - AjaxService doesn't know where to send queries.
     * It adds synchronous query into queue.
     */
    AjaxService.prototype.loadUrlMapper = function () {
        var _this = this;
        this.reqForUrlMapperSent = true;
        var subject = new Subject_1.Subject();
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
        subject.subscribe(function (data) {
            console.info('-->AjaxService->Received urlsMapper');
            _this.urlsMapper = data;
        });
        setTimeout(function () {
            _this.mapQueue();
        }, 10);
    };
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
    AjaxService.prototype.query = function (req) {
        var _this = this;
        // TODO REMAKE - delete blackBox
        var blackBox = new Subject_1.Subject();
        this.counter += 1;
        var pid = 'request_' + this.counter;
        this.loading.show(pid);
        console.log('HTTP Request', req);
        this.http.request(req)
            .map(function (res) {
            var body = res.json();
            var resp = new ServerResponse();
            _.extend(resp, body);
            // TODO Add request meta into Response
            console.log(resp);
            console.log(body);
            return resp;
        }).subscribe(// TODO check unsubscribe for blackbox subscription
        function (res) {
            _this.loading.hide(pid);
            if (res.hasError()) {
                _this.handleSiteError(res, blackBox);
            }
            else {
                blackBox.next(res.data);
            }
        }, function (err) {
            _this.loading.hide(pid);
            _this.handleServerError(err, blackBox);
        });
        return blackBox;
    };
    /**
     * Handles application error and runs .error() method on query 'BlackBox'.
     * If this error is auth error - runs this.auth.logoutByBackend()
     * @param res
     * @param blackBox
     */
    AjaxService.prototype.handleSiteError = function (res, blackBox) {
        // TODO Show error at view
        console.log(res);
        if (res.isAuthError() && this.auth) {
            console.log("App data:" + res.getData());
            this.auth.logoutByBackend();
            console.error('App Error message: ' + res.getError());
        }
        else {
            blackBox.error(res.getError());
        }
    };
    /**
     * Handles specific errors - server errors.
     * Runs error callback on higher subscribers.
     * @param error
     * @param blackBox
     */
    AjaxService.prototype.handleServerError = function (error, blackBox) {
        // TODO handlers for ERROR TYPES
        console.log(error);
        if (error.status === 500) {
        }
        else if (error.status === 404) {
        }
        // TODO Show error at view
        console.error('Server Error message: ' + error.status);
        blackBox.error(error.status);
    };
    /**
     * Returns string url for url_id. Source of urls - this.urlsMapper.
     * If can't get url path - returns null.
     * @param url_id
     * @returns {String}
     */
    AjaxService.prototype.getUrl = function (url_id) {
        return url_id;
        //return (url_id && this.urlsMapper && this.urlsMapper[url_id])
        //    ? this.urlsMapper[url_id].url : null;
    };
    /**
     * Low-level method for creating Request object for Angular Http Service.
     * Creates request object with body in JSON format.
     * Default request method = POST
     * @param options {url: string, method: string, data: any}
     * @returns {Request}
     */
    AjaxService.prototype.makeRequestInst = function (options) {
        var reqOpt = new http_1.BaseRequestOptions();
        var headers = new http_1.Headers();
        var obj_for_merge = {
            'url': options['url']
        };
        var method = http_1.RequestMethod.Post;
        console.log('Request Method', options.method);
        if (options.method && options.method != 'post') {
            switch (options.method) {
                case 'get':
                    method = http_1.RequestMethod.Get;
                    break;
                case 'put':
                    method = http_1.RequestMethod.Put;
                    break;
                case 'delete':
                    method = http_1.RequestMethod.Delete;
                    break;
                case 'head':
                    method = http_1.RequestMethod.Head;
                    break;
            }
        }
        obj_for_merge['method'] = method;
        if (method === http_1.RequestMethod.Post) {
            // obj_for_merge['body'] = {
            //     'params': options.data
            // }; //let body = JSON.stringify({ name });
            obj_for_merge['body'] = JSON.stringify(options.data);
            headers.append('Content-Type', 'application/json;charset=UTF-8');
            obj_for_merge['headers'] = headers;
        }
        else if (method === http_1.RequestMethod.Get) {
            if (_.isString(options.data)) {
                obj_for_merge['search'] = options.data;
            }
            else if (_.isObject(options.data)) {
                obj_for_merge['search'] = this.objectToQueryString(options.data);
            }
            else {
                console.error('Can\'t procced value!');
            }
        }
        else {
            console.error('Have no such method!');
        }
        return new http_1.Request(reqOpt.merge(obj_for_merge));
    };
    /**
     * Transforms input variable in safe query string.
     * It uses encodeURIComponent() method.
     * It doesn't include variable into result structure if value
     * equals null or undefined!
     * @param obj
     * @returns {string}
     */
    AjaxService.prototype.objectToQueryString = function (obj) {
        var qs = _.reduce(obj, function (result, value, key) {
            if (!_.isNull(value) && !_.isUndefined(value)) {
                if (_.isArray(value)) {
                    result += _.reduce(value, function (result1, value1) {
                        if (!_.isNull(value1) && !_.isUndefined(value1)) {
                            result1 += key + '=' + value1 + '&';
                            return result1;
                        }
                        else {
                            return result1;
                        }
                    }, '');
                }
                else {
                    result += encodeURIComponent(key.toString()) + '=' +
                        encodeURIComponent(value.toString()) + '&';
                }
                return result;
            }
            else {
                return result;
            }
        }, '').slice(0, -1);
        return qs;
    };
    ;
    AjaxService = __decorate([
        core_1.Injectable()
    ], AjaxService);
    return AjaxService;
}());
exports.AjaxService = AjaxService;
