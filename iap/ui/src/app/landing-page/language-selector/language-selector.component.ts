import {
    Component,
    OnChanges,
    Input,
    Output,
    SimpleChanges,
    EventEmitter,
} from '@angular/core';

import { LanguageItem } from "../../app.model"

@Component({
    selector: 'language-selector',
    templateUrl: './language-selector.component.html',
    styleUrls: ['./language-selector.component.css']
})
export class LanguageSelectorComponent implements OnChanges {

    private currLangId: string = null;
    @Input() languages: LanguageItem[] = [];
    @Output() changed: EventEmitter<string> = new EventEmitter();

    constructor() {
    }


    ngOnChanges(changes: SimpleChanges) {
        if (changes['languages']) {
            console.log('lang_changed');
            let l = changes['languages']['currentValue'].length;
            for (let i = 0; i < l; i++) {
                let item = changes['languages']['currentValue'][i]
                if (item['selected']) {
                    this.currLangId = item['id'];
                }
            }
            if (this.currLangId === null && changes['languages']['currentValue'][0]) {
                this.currLangId = changes['languages']['currentValue'][0]['id'];
                changes['languages']['currentValue'][0]['selected'] = true;
            }
        }
    }

    private onChangedLang(langId: string) {
        if (langId) {
            let exists = this.languages.filter((el) => {
                return (el['id'] == langId);
            }, this);
            if (exists.length) {
                this.currLangId = langId;
                this.changed.emit(langId);
            }
        }
    }

}
