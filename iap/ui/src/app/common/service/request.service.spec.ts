/* tslint:disable:no-unused-variable */

import { addProviders, async, inject } from '@angular/core/testing';
import { RequestService } from './request.service';

describe('Service: Request', () => {
  beforeEach(() => {
    addProviders([RequestService]);
  });

  it('should ...',
    inject([RequestService],
      (service: RequestService) => {
        expect(service).toBeTruthy();
      }));
});
