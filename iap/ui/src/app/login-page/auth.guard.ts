import {Injectable}  from '@angular/core';
import {CanActivate, CanActivateChild, Router,
    ActivatedRouteSnapshot, RouterStateSnapshot} from '@angular/router';
import {Observable} from 'rxjs/Observable';

import {AuthService} from "./auth.service";


@Injectable()
/**
 * Guard for defending routes from unauthorized users.
 * (ONLY) It is used for configuring Angular Router's routes
 */
export class AuthGuard implements CanActivate, CanActivateChild {

    constructor(private auth: AuthService, private router: Router) {}

    /**

     * Check user's logged in status and if not logged in - redirects to login-page.
     * Uses AuthService to define login-page status.
     * @param route
     * @param state
     *
     * @returns {boolean}
     */
    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        if (!this.auth.isLoggedIn())
        {
            this.router.navigate(['/login_page'], { queryParams: { returnUrl: state.url }});
            return false;
        }
        return true;
    }

    /**
     * The same as canActivate but for child path.
     * @param route
     * @param state
     * @returns {boolean}
     */
    canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        return this.canActivate(route, state);
    }
}




