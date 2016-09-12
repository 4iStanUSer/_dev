import { Injectable } from '@angular/core';
import {Observable} from "rxjs";

import {User} from "../cmp/login-widget/user";


@Injectable()
export class LoginService {

  constructor() { }
  getUsers(): Observable<User[]> {
      return new Observable<User[]>(resolve =>
          setTimeout(() => resolve(USERS), 2000) // 2 seconds
      );
  }
  doLogin(data:any): void {   }
}

//mock-users
export const USERS: User[] = [
    { id: 11, email: 'mrnice@mail.com', password: '' },
    { id: 12, email: 'narco@mail.com', password: '' },
    { id: 13, email: 'bombasto@mail.com', password: '' },
    { id: 14, email: 'celeritas@mail.com', password: '' },
    { id: 15, email: 'magneta@mail.com', password: '' },
    { id: 16, email: 'rubberman@mail.com', password: '' },
    { id: 17, email: 'dynama@mail.com', password: '' },
    { id: 18, email: 'dr_iq@mail.com', password: '' },
    { id: 19, email: 'magma@mail.com', password: '' },
    { id: 20, email: 'tornado@mail.com', password: '' }
];
