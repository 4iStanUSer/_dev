/* tslint:disable:no-unused-variable */

import {addProviders, async, inject} from '@angular/core/testing';
import {LoadingService} from './loading.service';

describe('Service: Loading', () => {
    beforeEach(() => {
        addProviders([LoadingService]);
    });

    it('should inject it dependencies',
        inject([LoadingService],
            (service: LoadingService) => {
                expect(service).toBeTruthy();
            }));

    it('should add(twice) to queue processes and then remove it',
        inject([LoadingService],
            (service: LoadingService) => {
                let processes = [
                    'proc_1',
                    'proc_2',
                    'proc_3',
                    'proc_4',
                    'proc_5',
                ];
                expect(service.getQueue().length == 0).toBe(true);
                for (let i = 0; i < processes.length; i++) {
                    service.show(processes[i]);
                }
                for (let i = 0; i < processes.length; i++) {
                    service.show(processes[i]);
                }
                expect(service.getQueue().length == 5).toBe(true);
                for (let i = 0; i < processes.length; i++) {
                    service.hide(processes[i]);
                }
                expect(service.getQueue().length == 0).toBe(true);
            }));
});
