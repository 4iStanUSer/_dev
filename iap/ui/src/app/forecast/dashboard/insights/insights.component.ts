import {Component, OnInit, OnChanges, Input, SimpleChanges} from '@angular/core';

interface InsightInput {
    type: string;
    text: string;
    disabled?: boolean;
}

class InsightModel {
    nomber: number;
    type: string;
    shortText: string;
    fullText: string;

    expanded: boolean = false;
    disabled: boolean = false;
    expandable: boolean = false;
}
class InsightsConfig { // TODO Implement configuration (VL)
    types: {
        [type: string]: {
            color: string;
        }
    }
}
class InsightsFilters { // TODO Implement filters (VL)

}

@Component({
    selector: 'insights',
    templateUrl: './insights.component.html',
    styleUrls: ['./insights.component.css']
})
export class InsightsComponent implements OnInit, OnChanges {

    private lang: Object = {
        'less_link': 'less',
        'more_link': 'read more'
    };
    private conf: Object = {
        'preview_length': 130
    };

    private storage: Array<InsightModel> = [];

    @Input() data: InsightInput;

    @Input() config: InsightsConfig;


    constructor() {
    }

    ngOnInit() {
    }

    ngOnChanges(ch: SimpleChanges) {
        if (ch['data']) {
            this.storage = [];
            let insights = ch['data']['currentValue'];
            for (let i=0; i<insights.length;i++) {
                let insight = new InsightModel();
                insight.nomber = i + 1;
                if (insights[i]['text'].length > this.conf['preview_length']) {
                    insight.shortText = this.getShortText(insights[i]['text']);
                    insight.expandable = true;
                } else {
                    insight.shortText = insights[i]['text'];
                    insight.expandable = false;
                }
                insight.fullText = insights[i]['text'];
                this.storage.push(insight);
            }
        }
        // TODO Implement other changes (VL)
    }

    onExpandButtonClick(insight: InsightModel, event: MouseEvent) {

        insight.expanded = !insight.expanded;
    }

    private getShortText(text: string) {
        let l = this.conf['preview_length'];
        let separators = [' ', ';', ':', '.', ','];
        if (text.length > l) {
            let i = l;
            let found = false;
            do {
                if (separators.indexOf(text[i]) != -1) {
                    found = true;
                } else {
                    i--;
                }
            } while (!found && i>=0);
            if (i>=0) {
                return text.slice(0, i) + '...';
            } else {
                return text.slice(0, l) + '...';
            }
        }
        return text;

    }

}
