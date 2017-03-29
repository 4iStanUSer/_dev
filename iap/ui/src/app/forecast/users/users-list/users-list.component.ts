import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';


import { IMultiSelectOption, IMultiSelectSettings, IMultiSelectTexts } from 'angular-2-dropdown-multiselect';
import { TableComponent } from "../../../common/cmp/table/table.component";

import { UserService } from './../user.service';
import { User, UserDetails, Role } from './../user.model';
import { LocalConfig } from './config';


@Component({
    templateUrl: './users-list.component.html',
    styleUrls: ['../users.component.css'],
    providers: [UserService]
})

export class UsersListComponent implements OnInit {
    public userForm: FormGroup; // our model driven form
    users: User[];
    optionsRoles: IMultiSelectOption[];
    config:Object = LocalConfig;
    current_user: UserDetails;
    show_create_new_user:boolean = false;

    @ViewChild(TableComponent)
    private tableComponent: TableComponent;

    options: Object = {
        logs: false,
        header_rows: [
            {
            name: 'first_name',
            label: 'First name',
            width: 30,
            sort: true,
            filter: true,
          },
          {
            name: 'last_name',
            label: 'Last name',
            width: 30,
            sort: true,
            filter: true,
          },
          {
            name: 'email',
            label: 'Email',
            width: 30,
            sort: true,
            filter: true,
          },
          {
            name: 'active',
            label: 'Active',
            width: 10,
            sort: false,
            filter: false,
          }
        ],
        default_sort: {
          field_name: 'first_name',
          order: true //true == 'ASC', false == 'DESC'
        },
        no_result_message: 'No result'
      };

    mySettings: IMultiSelectSettings = {
        pullRight: false,
        enableSearch: false,
        checkedStyle: 'checkboxes',
        buttonClasses: 'btn btn-default',
        selectionLimit: 0,
        closeOnSelect: false,
        showCheckAll: true,
        showUncheckAll: true,
        dynamicTitleMaxItems: 10,
        maxHeight: '300px',
    };

    myTexts: IMultiSelectTexts = {
        checkAll: 'Check all',
        uncheckAll: 'Uncheck all',
        checked: 'checked',
        checkedPlural: 'checked',
        searchPlaceholder: 'Search...',
        defaultTitle: 'Select Roles',
    };

    constructor(private _userService: UserService) { }

    // Load users
    _getUsers():void {
        this._userService.getUsers()
            .then(users => this.users = users);
    }

    // Load roles
    _getRoles():void {
        this._userService.getRoles()
            .then(roles => this.optionsRoles = roles);
    }

    // Load user details
    _getUserDetails(user_id:number):void {
        this._userService.getUserDetails(user_id)
            .then(result => {
                this.current_user = result;
                this._initForm(result);
            });
    }

    // Merge local and global config
    _updateConfig(new_config:Object) {
        this.config = Object.assign({}, this.config, new_config);
    }

    // Load global config and merge with local config
    _initConfig():void {
        this._userService.getConfig('users-list')
            .then(conf => this._updateConfig(conf));
    }

    _initForm(user: UserDetails):void {
        if (user) {
            // the long way
            this.userForm = new FormGroup({
                first_name: new FormControl(user.first_name, [Validators.required]),
                last_name: new FormControl(user.last_name, [Validators.required]),
                email: new FormControl(user.email, [Validators.required]),
                active: new FormControl(user.active),
                roles: new FormControl(user.roles)
            });
        } else {
            // the long way
            this.userForm = new FormGroup({
                first_name: new FormControl('', [Validators.required]),
                last_name: new FormControl('', [Validators.required]),
                email: new FormControl('', [Validators.required]),
                active: new FormControl(true),
                roles: new FormControl([])
            });
        }
    }

    ngOnInit():void {
        this._initConfig();
        this._getUsers();
        this._getRoles();
        this._initForm(this.current_user);
    }

    getCurrentId(user_id):void {
        this._getUserDetails(user_id);
        this.show_create_new_user = false;
        this.userForm.controls['roles'].valueChanges
            .subscribe((selectedOptions) => {
                this.current_user.roles = selectedOptions;
            });
     }

    onShowInput(event):void {
        let current_element = event.target;
        current_element.classList.add("hide");
        let current_input = current_element.parentNode.getElementsByTagName('input')[0];
        current_input.classList.remove("hide");
        current_input.focus();
    }

    onHideInput(event: any, key:string):void {
        let current_element = event.target;
        let current_span = current_element.parentNode.getElementsByTagName('span')[0];
        this.current_user[key] = current_element.value; // TODO add validation after change value
        if (current_element.value.length > 0) {
            current_span.classList.remove("hide");
            current_element.classList.add("hide");
        }
    }

    onResetPassword(event):void  {
        event.preventDefault();
        console.log('------ onResetPassword', this.current_user.id);
    }

    onShowCreateNewUser(event):void  {
        event.preventDefault();
        this.tableComponent.clearSelect();
        this.show_create_new_user = true;
        this.current_user = {
            id: 0, first_name: '', last_name: '', email: '', active: true, roles: [], avatar: ''
        }
        this._initForm(this.current_user);
    }

    onDeleteUser(event):void {
        event.preventDefault();
        this._userService.deleteUser(this.current_user.id);
        this.current_user = null;
        this.tableComponent.clearSelect();
    }

    onSubmit():void  {
        if (this.current_user.id === 0) {
            this._userService.createUser(this.current_user);
        } else {
            this._userService.editUser(this.current_user);
        }
        // TODO add notification
        this.tableComponent.clearSelect();
        this.show_create_new_user = false;
        this.current_user = null;
        this.tableComponent.onUpdateData();
    }
}
