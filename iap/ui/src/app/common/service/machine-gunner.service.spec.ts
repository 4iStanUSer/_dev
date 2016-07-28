/* tslint:disable:no-unused-variable */

import { addProviders, async, inject } from '@angular/core/testing';
import { MachineGunnerService } from './machine-gunner.service';

describe('Service: MachineGunner', () => {
  beforeEach(() => {
    addProviders([MachineGunnerService]);
  });

  it('should ...',
    inject([MachineGunnerService],
      (service: MachineGunnerService) => {
        expect(service).toBeTruthy();
      }));
});
