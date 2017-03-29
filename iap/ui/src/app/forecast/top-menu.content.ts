import { MenuItem } from "../app.model"

export const TOP_MENU_CONTENT: MenuItem[] = [
    {
        key: 'home',
        name: 'Home',
        disabled: false,
        path: '/forecast/landing'
    },
    {
        key: 'dashboard',
        name: 'Dashboard',
        disabled: false,
        path: '/forecast/dashboard'
    },
    {
        key: 'comparison',
        name: 'Comparison',
        disabled: false,
        path: '/forecast/comparison'
    },
    {
        key: 'scenarios',
        name: 'Scenarios',
        disabled: false,
        path: '/forecast/scenarios'
    },
    {
        key: 'simulator',
        name: 'Simulator',
        disabled: false,
        path: '/forecast/simulator'
    },
    {
        key: 'users',
        name: 'Users',
        disabled: false,
        path: '/forecast/users'
    }
];
