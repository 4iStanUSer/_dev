export class User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  active: boolean;

  constructor(id, first_name, last_name, email, active) {
    this.id = id;
    this.first_name = first_name;
    this.last_name = last_name;
    this.email = email;
    this.active = active;
  }
}

export class UserDetails {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  active: boolean;
  roles: number[];
  avatar: string;

  constructor(id, first_name, last_name, email, active) {
    this.id = id;
    this.first_name = first_name;
    this.last_name = last_name;
    this.email = email;
    this.active = active;
    this.roles = [1,2];
    this.avatar = '';
  }
}

export class Role {
    id: number;
    name: string;
    description?: string;
}
