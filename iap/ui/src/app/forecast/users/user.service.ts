import { Injectable } from '@angular/core';
import { IMultiSelectOption, IMultiSelectSettings, IMultiSelectTexts } from 'angular-2-dropdown-multiselect';

import { User, UserDetails, Role } from './user.model';
import { USER, USERS, ROLES, CONFIG } from './mock';


@Injectable()
export class UserService {
  getUsers(): Promise<User[]> {
      return Promise.resolve(USERS);
  }

  getRoles(): Promise<IMultiSelectOption[]> {
      return Promise.resolve(ROLES);
  }

  getUserDetails(user_id:number): Promise<any> {
      let user_details: UserDetails;
      let current_user = USERS.filter(item => item.id === user_id)[0];
      if (current_user !== undefined) {
          user_details = new UserDetails(
              current_user['id'],
              current_user.first_name,
              current_user.last_name,
              current_user.email,
              current_user.active
          );
      }
      return Promise.resolve(user_details);
  }

  createUser(data: UserDetails){
      let new_user = new User (
              new Date().getTime(),
              data.first_name,
              data.last_name,
              data.email,
              data.active
          );
      USERS.push(new_user);
  }

  editUser(data: UserDetails){
      let new_user = new User (
              data.id,
              data.first_name,
              data.last_name,
              data.email,
              data.active
          );

      for (let i=0; USERS.length > i; i++) {
          if (USERS[i].id === new_user.id) {
              USERS[i] = new_user;
              break;
          }
      }
  }

  deleteUser(user_id:number){
      for (let i=0; USERS.length > i; i++) {
          if (USERS[i].id === user_id) {
              USERS.splice(i, 1);
              break;
          }
      }
  }

  getConfig(key:string): Promise<any> {
      let conf_list = CONFIG.filter(conf_item => conf_item.configuration_key === key);
      if (conf_list.length === 0) {
          return Promise.resolve(null);
      }
      return Promise.resolve(conf_list[0]);
  }
}
