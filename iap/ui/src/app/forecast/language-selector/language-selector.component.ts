import {
    Component,
    OnInit,
    OnChanges,
    Input,
    Output,
    SimpleChanges,
    EventEmitter,
} from '@angular/core';

export type LanguageSelectorInput = Array<{
    id: string;
    name: string;
    selected?: boolean
}>;
export type LanguageSelectorOutput = {
    lang_id: string;
}

@Component({
    selector: 'language-selector',
    templateUrl: './language-selector.component.html',
    styleUrls: ['./language-selector.component.css']
})
export class LanguageSelectorComponent implements OnInit, OnChanges {

    private currLangId: string = null;

    @Input() langs: LanguageSelectorInput = [];

    @Output() changed: EventEmitter<LanguageSelectorOutput> = new EventEmitter();

    constructor() {
    }

    ngOnInit() {
    }

    ngOnChanges(ch: SimpleChanges) {
        console.info('LanguageSelectorComponent: ngOnChanges()');

        if (ch['langs']) {
            let l = ch['langs']['currentValue'].length;
            for (let i = 0; i < l; i++) {
                if (ch['langs']['currentValue'][i]['selected']) {
                    this.currLangId = ch['langs']['currentValue'][i]['id'];
                }
            }
            if (this.currLangId === null && ch['langs']['currentValue'][0]) {
                this.currLangId = ch['langs']['currentValue'][0]['id'];
                ch['langs']['currentValue'][0]['selected'] = true;
            }
        }
    }

    private onChangedLang(langId: string) {
        if (langId) {
            let exists = this.langs.filter((el) => {
                return (el['id'] == langId);
            }, this);
            if (exists.length) {
                this.currLangId = langId;
                this.changed.emit({
                    lang_id: langId
                });
            }
        }
    }

}
