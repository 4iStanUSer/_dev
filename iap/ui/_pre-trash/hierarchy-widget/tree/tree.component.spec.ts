/* tslint:disable:no-unused-variable */

// import {By}           from '@angular/platform-browser';
// import {DebugElement} from '@angular/core';
// import {
//     addProviders,
//     async,
//     inject,
//     TestComponentBuilder,
//     beforeEachProviders
// } from '@angular/core/testing';
// import {TreeComponent, TreeNodeComponent} from './tree.component';
//
// // class MockLoginService extends LoginService {
// //   login(pin: number) {
// //     return Promise.resolve(true);
// //   }
// // }
//
// describe('Component: Tree', () => {
//
//     // it('should create an instance', () => {
//     //     let component = new TreeComponent();
//     //     expect(component).toBeTruthy();
//     // });
//
//     // it('should render hierarchy tree', async(inject([TestComponentBuilder], (tcb) => {
//     //     console.log(tcb);
//     //     tcb
//     //         .createAsync(TreeComponent).then(function (fixture) {
//     //         console.log(2);
//     //         let tree = fixture.componentInstance,
//     //             element = fixture.nativeElement;
//     //         fixture.detectChanges();
//     //         expect(true).toBe(true);
//     //         fixture.destroy();
//     //     })
//     //
//     // })));
//
//
//     let tcb;
//
//     let baseTree = [
//         {
//             "id": 1, "text": "Parent node 1", "type": "parent",
//             "state": {
//                 "opened": true,
//                 "disabled": false,
//                 "selected": true
//             },
//             "children": [
//                 {
//                     "id": 3, "text": "Child node 1.1", "type": "child",
//                     "children": false
//                 },
//                 {
//                     "id": 4, "text": "Child node 1.2", "type": "child",
//                     "children": false
//                 }
//             ]
//         },
//         {
//             "id": 2, "text": "Parent node 2", "type": "parent",
//             "state": {
//                 "opened": false,
//                 "disabled": false,
//                 "selected": false
//             },
//             "children": [
//                 {
//                     "id": 5, "text": "Child node 2.1", "type": "child",
//                     "children": false
//                 },
//                 {
//                     "id": 6, "text": "Child node 2.2", "type": "child",
//                     "children": false
//                 }
//             ]
//         }
//     ];
//
//     beforeEach(() => {
//         addProviders([
//             TestComponentBuilder,
//             TreeComponent
//             // provide(LoginService, {useClass: MockLoginService}),
//             // UserService
//         ]);
//     });
//     beforeEach(inject([TestComponentBuilder], _tcb => {
//         tcb = _tcb
//     }));
//
//     it('should renders tree and find "Parent node 1" at first position', done => {
//         tcb.createAsync(TreeComponent).then(fixture => {
//             let cmp = fixture.componentInstance,
//                 element = fixture.nativeElement;
//             cmp.items = baseTree;
//             fixture.detectChanges();
//             expect(element.querySelector('.node-content-wrapper').innerText).toBe('Parent node 1');
//             done();
//         })
//             .catch(e => done.fail(e));
//     });
//
//     it('should be shown only opened nodes', done => {
//         tcb.createAsync(TreeComponent).then(fixture => {
//             let cmp = fixture.componentInstance,
//                 element = fixture.nativeElement;
//             cmp.items = baseTree;
//             fixture.detectChanges();
//             expect(element.querySelector('.tree')).not.toContain('Child node 2.1');
//             done();
//         })
//             .catch(e => done.fail(e));
//     });
//
//     it('should - nodes with children must be collapsible', done => {
//         tcb.createAsync(TreeComponent).then(fixture => {
//             let cmp = fixture.componentInstance,
//                 element = fixture.nativeElement;
//             cmp.items = baseTree;
//             fixture.detectChanges();
//             let parentNode = element.querySelector('tree-node:nth-of-type(2) .tree-node-level-1');
//             let expandButton = parentNode.querySelector('.toggle-children-button');
//
//             // expect(parentNode).not.toContain('.tree-children');
//             expect(!!parentNode.querySelector('.tree-children')).toBe(false);
//             expandButton.click();
//             fixture.detectChanges();
//             expect(!!parentNode.querySelector('.tree-children')).toBe(true);
//             done();
//         })
//             .catch(e => done.fail(e));
//     });
//
//     it('should node must be selected if clicked', done => {
//         tcb.createAsync(TreeComponent).then(fixture => {
//             let cmp = fixture.componentInstance,
//                 element = fixture.nativeElement;
//             cmp.items = baseTree;
//             fixture.detectChanges();
//
//             let node = element.querySelector('tree-node:nth-of-type(2) .tree-node-level-1');
//             expect(node.className.indexOf('tree-node-active') == -1).toBe(true);
//             node.querySelector('.node-content-wrapper').click();
//             fixture.detectChanges();
//             expect(node.className.indexOf('tree-node-active') == -1).toBe(false);
//             done();
//         })
//             .catch(e => done.fail(e));
//     });
// });
