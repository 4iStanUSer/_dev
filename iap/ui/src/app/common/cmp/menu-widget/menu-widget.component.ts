import { Component, Input, Output, OnInit, EventEmitter } from '@angular/core';
import * as _ from 'lodash';

interface IMenuItem {
    name: string;
    disabled: boolean;
    children: Array<IMenuItem>;
}

@Component({
  // moduleId: module.id,
  selector: 'menu-widget',
  templateUrl: 'menu-widget.component.html',
  styleUrls: ['menu-widget.component.css']
})
export class MenuWidgetComponent implements OnInit {

    @Input() items: Array<IMenuItem>;
    @Output() menuClicked = new EventEmitter();

    ngOnInit() { }

    public addNewItem(data) {
        let newItem = null;
        let position = null;
        if (data && data['newItem'] && _.isArray(this.items)) {
            newItem = data['newItem'];
            if ('position' in data && data['position'] != null
                && !isNaN(data['position'])) {
                position = parseInt(data['position']);
                this.items.splice(position, 0, newItem);
            } else {
                this.items.push(newItem);
            }
            return true;
        }
        return false;
    }

    /**
     * Handler for click on any menu item and raise event menuClicked.
     * @param event
     * @param item
     */
    private _onClickItem(e: Event, item: IMenuItem) {
        e.preventDefault();
        // && !item.disabled
        if (item && !e.srcElement.classList.contains('caret')) {
            this.menuClicked.emit(item);
        }
    }

    private _onClickCaret(e: Event) {
        e.preventDefault();
        e.stopPropagation()
    }

}
