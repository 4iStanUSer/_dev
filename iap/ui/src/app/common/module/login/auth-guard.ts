import {Injectable}  from '@angular/core';
import {
    CanActivate,
    CanActivateChild,
    Router,
    ActivatedRouteSnapshot,
    RouterStateSnapshot
} from '@angular/router';

import {Observable} from 'rxjs/Observable';

import {AuthService} from "../../service/auth.service";
import {AjaxService} from "../../service/ajax.service";

@Injectable()
/**
 * Guard for defending routes from unauthorized users.
 * (ONLY) It is used for configuring Angular Router's routes
 */
export class AuthGuard implements CanActivate, CanActivateChild {

    constructor(private req: AjaxService,
                private auth: AuthService,
                private router: Router) {
    }

    /**
     * Check user's logged in status and if not logged in - redirects to login.
     * Uses AuthService to define login status.
     * @param route
     * @param state
     * @returns {Observable<boolean>}
     */
    canActivate(route: ActivatedRouteSnapshot,
                state: RouterStateSnapshot): Observable<boolean> {
        console.log('AuthGuard#canActivate called');
        let url: string = state.url;
        console.log(state.url);
        return this.auth.isLoggedIn().map(e => {
                if (e) {
                    return true;
                }
                else {
                 this.auth.redirectUrl = url;
                 this.router.navigate(['/login']);
                 return Observable.of(false);
                }
            });
            // .catch(() => {
            //     this.auth.redirectUrl = url;
            //     this.router.navigate(['/login']);
            //     return Observable.of(false);
            // });
    }

    canActivateChild(route: ActivatedRouteSnapshot,
                     state: RouterStateSnapshot): Observable<boolean> {
        console.log('AuthGuard#canActivateChild called');
        return this.canActivate(route, state);
    }
}
