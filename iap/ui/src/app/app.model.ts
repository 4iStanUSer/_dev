export class Tool {
    id: string;
    name: string;
    description: string;
    icon: string;
    projects: Project[] = [];

    init(input: Object): void {
        if (input['name']) {
            this.name = input['name'];
        }
        if (input['description']) {
            this.description = input['description'];
        }
        if (input['icon']) {
            this.icon = input['icon'];
        }
    }
}

export class Project {
    id: string;
    name: string;
    description: string;
    icon: string;

    init(input: Object): void {
        if (input['id']) {
            this.id = input['id'];
        }
        if (input['name']) {
            this.name = input['name'];
        }
        if (input['description']) {
            this.description = input['description'];
        }
        if (input['icon']) {
            this.icon = input['icon'];
        }
    }
}

export class User{
    id: string;
    name: string;
    email: string;

    init(input: Object): void {
        if (input['id']) {
            this.id = input['id'];
        }
        if (input['name']) {
            this.name = input['name'];
        }
        if (input['email']) {
            this.name = input['name'];
        }
    }
}

export class Client {
    id: string;
    name: string;
    icon: string;

    init(input: Object): void {
        if (input['id']) {
            this.id = input['id'];
        }
        if (input['name']) {
            this.name = input['name'];
        }
        if (input['icon']) {
            this.icon = input['icon'];
        }
    }
}

export class MenuItem {
    key: string = null;
    name: string = null;
    disabled: boolean = false;
    path: string = null;
}

export class LanguageItem {
    id: string;
    name: string;
    selected: boolean;
}
