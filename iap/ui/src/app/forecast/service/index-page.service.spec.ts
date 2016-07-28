/* tslint:disable:no-unused-variable */

import { addProviders, async, inject } from '@angular/core/testing';
import { IndexPageService } from './index-page.service';

describe('Service: IndexPage', () => {
  beforeEach(() => {
    addProviders([IndexPageService]);
  });

  it('should ...',
    inject([IndexPageService],
      (service: IndexPageService) => {
        expect(service).toBeTruthy();
      }));
});
