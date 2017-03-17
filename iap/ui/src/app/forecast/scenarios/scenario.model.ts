export class ScenarioModel {
    id: number = null;
    author: string = null;
    criteria: string = null;
    name: string = null;
    description: string = null;
    favorite: string = null;
    modify_date: string = null;
    deadline: string = null;
    shared: string = null;
    status: string = null;
    scenario_permission: string[] = null;

    constructor(id: number, author: string, criteria: string, name: string, description: string,
                favorite: string, modify_date: string, deadline: string, shared: string, status: string,
                scenario_permission: string[]) {
        this.id = id;
        this.author = author;
        this.criteria = criteria;
        this.name = name;
        this.description = description;
        this.favorite = favorite;
        this.modify_date = modify_date;
        this.deadline = deadline;
        this.shared = shared;
        this.status = status;
        this.scenario_permission = scenario_permission;
    }

    /**
     * Check scenario permission
     * @param permission: string
     * @return boll: if permission in scenario_permission => true else => false
     */
    checkPermission(permission) {
        console.log('---checkPermission', this.scenario_permission);
        if (this.scenario_permission.find(permission) === undefined) {
            return false;
        } else {
            return true;
        }
    }
}

export class ScenarioDetailsModel {
    modify_date: string;
    selectors: { key: string, values: string[] }[] = [];
    table: { drivers: string, growth: string }[] = [];
    main_info: {name: string, value: string}[] = [];
}
