import { User, UserDetails, Role } from './user.model';
import { IMultiSelectOption, IMultiSelectSettings, IMultiSelectTexts } from 'angular-2-dropdown-multiselect';

export const USER: UserDetails = {
    id: 2, first_name: 'Mr. Nice2 first_name', last_name: 'Mr. Nice2 last_name', email: 'test@test2.ua',
    active: true, roles: [2,3], avatar: 'asd'
};

export const USERS: User[] = [
  {id: 1, first_name: 'Mr. Nice', last_name: 'Mr. Nice', email: 'test@test.ua', active: true},
  {id: 2, first_name: 'Mr. Nice2', last_name: 'Mr. Nice22', email: 'test@test2.ua', active: true},
  {id: 3, first_name: 'Mr. Nice3', last_name: 'Mr. Nice3', email: 'test@test3.ua', active: false},
  {id: 4, first_name: 'Mr. Nice4', last_name: 'Mr. Nice44', email: 'test@test.ua', active: false},
  {id: 5, first_name: 'Mr. Nice5', last_name: 'Mr. Nice2', email: 'test@test2.ua', active: true},
  {id: 6, first_name: 'Mr. Nice6', last_name: 'Mr. Nice3', email: 'test@test3.ua', active: true},
  {id: 7, first_name: 'Mr. Nice7', last_name: 'Mr. Nice', email: 'test@test.ua', active: false},
  {id: 8, first_name: 'Mr. Nice8', last_name: 'Mr. Nice2', email: 'test@test2.ua', active: true},
  {id: 9, first_name: 'Mr. Nice9', last_name: 'Mr. Nice3', email: 'test@test3.ua', active: false},
  {id: 10, first_name: 'Mr. Nice10', last_name: 'Mr. Nice', email: 'test@test.ua', active: true},
  {id: 11, first_name: 'Mr. Nice11', last_name: 'Mr. Nice2', email: 'test@test2.ua', active: true},
  {id: 12, first_name: 'Mr. Nice12', last_name: 'Mr. Nice3', email: 'test@test3.ua', active: false},
  {id: 13, first_name: 'Mr. Nice13', last_name: 'Mr. Nice', email: 'test@test.ua', active: true},
  {id: 14, first_name: 'Mr. Nice14', last_name: 'Mr. Nice2', email: 'test@test2.ua', active: true},
  {id: 15, first_name: 'Mr. Nice15', last_name: 'Mr. Nice3', email: 'test@test3.ua', active: false},
  {id: 16, first_name: 'Mr. Nice16', last_name: 'Mr. Nice', email: 'test@test.ua', active: true},
  {id: 17, first_name: 'Mr. Nice17', last_name: 'Mr. Nice2', email: 'test@test2.ua', active: true},
  {id: 18, first_name: 'Mr. Nice18', last_name: 'Mr. Nice3', email: 'test@test3.ua', active: false},
  {id: 19, first_name: 'Mr. Nice19', last_name: 'Mr. Nice', email: 'test@test.ua', active: true},
  {id: 20, first_name: 'Mr. Nice20', last_name: 'Mr. Nice2', email: 'test@test2.ua', active: true},
  {id: 21, first_name: 'Mr. Nice21', last_name: 'Mr. Nice3', email: 'test@test3.ua', active: false},
  {id: 22, first_name: 'Mr. Nice22', last_name: 'Mr. Nice', email: 'test@test.ua', active: true},
  {id: 23, first_name: 'Mr. Nice23', last_name: 'Mr. Nice2', email: 'test@test2.ua', active: false},
  {id: 24, first_name: 'Mr. Nice24', last_name: 'Mr. Nice3', email: 'test@test3.ua', active: true}
];


export const ROLES: IMultiSelectOption[] = [
    {id: 1, name: 'Admin'},
    {id: 2, name: 'Manager'},
    {id: 3, name: 'User'}
];


export const CONFIG: any[] = [
    {
        "configuration_key": "users-list",
        "create_user_label": "Create New User --global",
    }
];
