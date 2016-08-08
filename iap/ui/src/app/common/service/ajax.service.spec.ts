/* tslint:disable:no-unused-variable */

import { addProviders, inject, async } from '@angular/core/testing';
import {MockBackend} from '@angular/http/testing';
import {ReflectiveInjector} from '@angular/core';
import {
    BaseRequestOptions,
    Response,
    ResponseOptions,
    ConnectionBackend,
    Http,
    Request
} from '@angular/http';
import 'rxjs/add/observable/from';
// import {provide} from '@angular/core';
// import {HTTP_PROVIDERS} from '@angular/http';
// import {
//     Http, Response, Request, RequestMethod, BaseRequestOptions,
//     Headers
// } from '@angular/http';
import {Observable}     from 'rxjs/Observable';

import {LoadingService} from './loading.service';
import {AjaxService} from './ajax.service';
import {MockConnection} from "@angular/http/testing/mock_backend";


class MockLoadingService extends LoadingService { }
class MockHttpService {
    request(req: Request) {
        let resp = new Response(
            new ResponseOptions({
                    body: JSON.stringify(
                        {
                            error: false,
                            data: [{
                                name: 'name',
                                id: 'id'
                            }]
                        }
                    )
                }
            ));

        return Observable.create(function (observer) {
            // console.log(observer);
            observer.next(resp);
            //observer.onCompleted();

            // // Note that this is optional, you do not have to return this if you require no cleanup
            // return Disposable.create(function () {
            //     console.log('disposed');
            // });
        });
        // return Observable.create(new Response(
        //         new ResponseOptions({
        //                 body: JSON.stringify(
        //                     {
        //                         error: false,
        //                         data: [{
        //                             name: 'name',
        //                             id: 'id'
        //                         }]
        //                     }
        //                 )
        //             }
        //         )));
    }
}

describe('Service: Ajax', () => {
    let mockbackend, service;


    beforeEach(() => {
        //jasmine.DEFAULT_TIMEOUT_INTERVAL = 10000;
        addProviders([
            AjaxService,
            MockBackend,
            BaseRequestOptions,
            // {provide: Http,
            //     useFactory: (mockbackend: MockBackend, //ConnectionBackend,
            //                  defaultOptions: BaseRequestOptions) => {
            //
            //         mockbackend.connections.subscribe(
            //             (connection: MockConnection) => {
            //                 connection.mockRespond(new Response(
            //                     new ResponseOptions({
            //                             body: JSON.stringify(
            //                                 {
            //                                     has_more: false,
            //                                     data: [{
            //                                         name: 'name',
            //                                         id: 'id'
            //                                     }]
            //                                 }
            //                             )
            //                         }
            //                     )));
            //             });
            //         return new Http(mockbackend, defaultOptions);
            //     },
            //     deps: [MockBackend, BaseRequestOptions]
            // },
            {provide: LoadingService, useClass: MockLoadingService},
            {provide: Http, useClass: MockHttpService},
            // {provide: Http,
            //   useFactory: (backend, options) => new Http(backend, options),
            //   deps: [MockBackend, BaseRequestOptions]},
            ]);
    });
    beforeEach(inject([MockBackend, AjaxService], (_mockbackend, _service) => {
        mockbackend = _mockbackend;
        service = _service;
    }));

    it('should inject own dependencies',
        inject([AjaxService],
            (service: AjaxService) => {
                expect(service).toBeTruthy();
            }));

    // it('should return mocked response', done => {
    //     let a = service.get({
    //         url: '/forecast/get_index_page_data',
    //         data: 'mock'
    //     });
    //     a.subscribe(languages => {
    //         console.log(languages);
    //         expect(languages).toContain('ru');
    //         expect(languages).toContain('es');
    //         expect(languages.length).toBe(2);
    //         done();
    //     });
    //
    //     // // let response = ["ru", "es"];
    //     // var conn;
    //     // mockbackend.connections.subscribe(connection => {
    //     //     conn = connection;
    //     //     connection.mockRespond(new Response(
    //     //         new ResponseOptions({
    //     //                 status: 200,
    //     //                 url: 'http://asd.com',
    //     //                 body: JSON.stringify(
    //     //                     {
    //     //                         error: false,
    //     //                         data: {
    //     //                             name: 'name',
    //     //                             id: 'id'
    //     //                         }
    //     //                     }
    //     //                 )
    //     //             }
    //     //         )));
    //     //     // connection.mockRespond(new Response({body: JSON.stringify(response)}));
    //     // });
    //
    //     //var backend = injector.get(MockBackend);
    //     // var http = injector.get(Http);
    //     // backend.connections.subscribe(c => connection = c);
    //     // http.request('something.json').subscribe(res => {
    //     //   text = res.text();
    //     // });
    //     // connection.mockRespond(new Response({body: 'Something'}));
    //     // expect(text).toBe('Something');
    //
    //     // mockbackend.connections.observer({
    //     //     next: connection => {
    //     //         var response = new Response( new ResponseOptions({
    //     //                 status: 200,
    //     //                 url: 'http://asd.com',
    //     //                 body: JSON.stringify(
    //     //                     {
    //     //                         error: false,
    //     //                         data: {
    //     //                             name: 'name',
    //     //                             id: 'id'
    //     //                         }
    //     //                     }
    //     //                 )
    //     //             }));
    //     //         setTimeout(() => {
    //     //             // Send a response to the request
    //     //             connection.mockRespond(response);
    //     //         });
    //     //     }
    //     // });
    //
    //
    // });
    // // it('should execute get method', done => {
    // //     inject([AjaxService],
    // //         (service: AjaxService) => {
    // //             // expect(service).toBeTruthy();
    // //             //expect(true).toBe(false);
    // //
    // //             service
    // //                 .get({
    // //                     url: '/forecast/get_index_page_data',
    // //                     data: 'mock'
    // //                 })
    // //                 .subscribe(
    // //                     (d) => {
    // //                         console.log(111);
    // //                         expect(d).toBe(false);
    // //                         done();
    // //                     },
    // //                     (d) => {
    // //                         console.log(222);
    // //                         expect(d).toBe(false);
    // //                         done();
    // //                     });
    // //         })
    // // });
    //
    // // it('should get a response', () => {
    // //     var connection; //this will be set when a new connection is emitted from the backend.
    // //     var text; //this will be set from mock response
    // //     var injector = ReflectiveInjector.resolveAndCreate([
    // //         MockBackend,
    // //         {
    // //             provide: Http, useFactory: (backend, options) => {
    // //             return new Http(backend, options);
    // //         }, deps: [MockBackend, BaseRequestOptions]
    // //         }]);
    // //     var backend = injector.get(MockBackend);
    // //     var http = injector.get(Http);
    // //     backend.connections.subscribe(c => connection = c);
    // //     http.request('something.json').subscribe(res => {
    // //         text = res.text();
    // //     });
    // //     var options = new ResponseOptions({
    // //         body: {name: 'Jeff'}
    // //     });
    // //     connection.mockRespond(new Response(options));
    // //
    // //     expect(text).toBe('Something');
    // // });
});
