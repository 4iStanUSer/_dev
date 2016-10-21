/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { SimulatorPageDataManagerService } from './simulator-page-data-manager.service';

describe('Service: SimulatorPageDataManager', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SimulatorPageDataManagerService]
    });
  });

  it('should ...', inject([SimulatorPageDataManagerService], (service: SimulatorPageDataManagerService) => {
    expect(service).toBeTruthy();
  }));
});
