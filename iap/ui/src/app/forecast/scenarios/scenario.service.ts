import { Injectable } from '@angular/core';


import { ScenarioDetails } from './mock'
import { ScenarioDetailsModel } from './scenario.model';


@Injectable()
export class ScenarioService {
  getScenarioDetails(id: number): ScenarioDetailsModel {
      console.log('---getScenarioDetails', id);
      return ScenarioDetails;
  }
}
