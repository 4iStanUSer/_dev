/* tslint:disable:no-unused-variable */

import { By }           from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
// import { ElementRef, Renderer } from '@angular/core';
import {
    // beforeEachProviders,
    // beforeEach,
    // describe,
    // expect,
    // it,
    async,
    inject,
    fakeAsync,
    TestComponentBuilder,
    addProviders,
    ComponentFixture
} from '@angular/core/testing';

// import { ElementRef, Renderer } from '@angular/core';
import { DropdownComponent } from './dropdown.component';

// import { AuthHttp } from 'angular2-jwt';
// import { Router } from '@angular/router';
// import { Http } from '@angular/http';
// import { LogoutButtonComponent } from './logout-button.component';
// import { UserService } from '../../services/index';

describe('Component: Dropdown', () => {

  // beforeEachProviders(() => [
  //   LogoutButtonComponent,
  //   MockBackend,
  //   provide(Http, {
  //     useFactory: (backend: MockBackend, defaultOptions: BaseRequestOptions) => {
  //       return new Http(backend, defaultOptions);
  //     },
  //     deps: [MockBackend, BaseRequestOptions]
  //   }),
  //   provide(AuthHttp, { useFactory: Http }),
  //   provide(AuthConfig, {useValue: new AuthConfig()}),
  //   ConnectionBackend
  // ]);

  // beforeEachProviders(() => [
  //   LogoutButtonComponent,
  //   UserService
  // ]);
    let dropdownCmp: DropdownComponent;
    let tcb;

    // beforeEach(inject([TestComponentBuilder], _tcb => {
    //     tcb = _tcb
    // }));
    // beforeEach(() => {
    //     dropdownCmp = new DropdownComponent(Renderer, ElementRef);
    // });
    // beforeEach(() => {
    //     addProviders([
    //         DropdownComponent,
    //         ElementRef,
    //         Renderer
    //     ]);
    // });

    // beforeEach(() => {
    //     addProviders([
    //         // ElementRef, Renderer
    //         provide(DropdownComponent, {
    //             useFactory: (rndr: Renderer, elRef: ElementRef) => {
    //                 return new DropdownComponent(rndr, elRef);
    //             },
    //             deps: [Renderer, ElementRef]
    //         }),
    //     ]);
    // });

    // it('should inject dependencies', async(inject([DropdownComponent],
    //     (component: DropdownComponent) => {
    //         expect(component).toBeTruthy();
    // })));

    // it('should inject own dependencies', async(inject([TestComponentBuilder], (tcb) => {
    //     (component: DropdownComponent) => {
    //         expect(component).toBeTruthy();
    //     }
    // })));
    // it('should inject own dependencies', async(inject([TestComponentBuilder], (tcb) => {
    //     (component: DropdownComponent) => {
    //         expect(component).toBeTruthy();
    //     }
    //     // tcb
    //     //   .createAsync(DropdownComponent).then(function(fixture) {
    //     //     fixture.detectChanges();
    //     //     expect(true).toBe(true);
    //     //     fixture.destroy();
    //     //   })
    //
    // })));


    //   //specs
    // it('should render `Hello World!`', done => {
    //   tcb.createAsync(Greeter).then(fixture => {
    //     let greeter = fixture.componentInstance,
    //       element = fixture.nativeElement;
    //     greeter.name = 'World';
    //     fixture.detectChanges(); //trigger change detection
    //     expect(element.querySelector('h1').innerText).toBe('Hello World!');
    //     done();
    //   })
    //   .catch(e => done.fail(e));
    // });
});



// import {inject, async, addProviders} from '@angular/core/testing';
// import {TestComponentBuilder, ComponentFixture} from '@angular/compiler/testing';
// import {Component} from '@angular/core';
// import {By} from '@angular/platform-browser';
//
// import { ElementRef, Renderer } from '@angular/core';
// import { DropdownComponent } from './dropdown.component';
//
// // import { By }           from '@angular/platform-browser';
// import { DebugElement } from '@angular/core';
// // import { addProviders, async, inject, TestComponentBuilder } from '@angular/core/testing';
// // import {TestComponentBuilder} from '@angular/compiler/testing';
//
//
// describe('Component: Dropdown', () => {
//     let fixture:ComponentFixture<any>;
//     let element:any;
//     let context:any;
//
//     beforeEach(() => [
//         TestComponentBuilder
//     ]);
//
//     it('should be closed by default', async(inject([TestComponentBuilder], (tcb) => {
//         const html = `<div ngbDropdown></div>`;
//
//         tcb.overrideTemplate(DropdownComponent, html).createAsync(DropdownComponent).then((fixture) => {
//             fixture.detectChanges();
//             const compiled = fixture.nativeElement;
//
//             expect(getDropdownEl(compiled)).toHaveCssClass('dropdown');
//             expect(getDropdownEl(compiled)).not.toHaveCssClass('open');
//         });
//     })));
//
//
//     // var dropdownCpm;
//     //
//     // // beforeEach(() => {
//     // //     addProviders([ElementRef, Renderer])
//     // // });
//     // beforeEach(inject([ElementRef, Renderer], (elRef, rndr) => {
//     //     dropdownCpm = new DropdownComponent(rndr, elRef);
//     // }));
//     // it('...', inject([AClass], (object) => {
//     //     object.doSomething();
//     //     expect(...);
//     // })
//     //
//     // beforeEach(injectAsync([TestComponentBuilder], (tcb: TestComponentBuilder) => {
//     //     return tcb
//     //         .overrideProviders(ListComponent, [provide(UserService, {useClass: MockUserService})])
//     //         .createAsync(ListComponent)
//     //         .then((componentFixture: ComponentFixture) => {
//     //         this.listComponentFixture = componentFixture;
//     //         });
//     // }));
//     //
//     // it('should create an instance', () => {
//     //     let component = new DropdownComponent();
//     //     expect(component).toBeTruthy();
//     // });
//
//
// });
//
//
// describe('ListComponent', () => {
//
//   it('should render list', injectAsync([TestComponentBuilder], (tcb: TestComponentBuilder) => {
//     return tcb.createAsync(ListComponent).then((componentFixture: ComponentFixture) => {
//       const element = componentFixture.nativeElement;
//       componentFixture.componentInstance.users = ['John'];
//       componentFixture.detectChanges();
//       expect(element.querySelectorAll('span').length).toBe(1);
//     });
//   }));
//
// });
