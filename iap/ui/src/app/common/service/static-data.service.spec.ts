/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { StaticDataService } from './static-data.service';

describe('Service: StaticData', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StaticDataService]
    });
  });

  it('should ...', inject([StaticDataService], (service: StaticDataService) => {
    expect(service).toBeTruthy();
  }));
});
