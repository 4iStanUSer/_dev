import { Injectable } from '@angular/core';
import { Subject }    from 'rxjs/Subject';
import { Observable } from 'rxjs/Observable';


@Injectable()
export class NotificationService {

  private subject= new Subject<any>();
  private response= new Subject<any>();

  setHeader(config: any): void {
    return this.subject.next(config);
  }


  getMessage(): Observable<any> {
      return this.subject.asObservable();

  }

  setResponse(button: any): void{
    return this.response.next(button);

  }

  getResponse(): Observable<any> {
      return this.response.asObservable();

  }



}
