/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { DataManagerService } from './data-manager.service';

describe('Service: DataManager', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DataManagerService]
    });
  });

  it('should ...', inject([DataManagerService], (service: DataManagerService) => {
    expect(service).toBeTruthy();
  }));
});
