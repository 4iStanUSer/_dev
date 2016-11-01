export interface TimePeriodInput {
    start: string;
    end: string;
    mid: string;
}

export class TimePeriodModel { // TODO Post TimeLabel Object
    constructor(
        public start: string,
        public end: string,
        public mid: string
    ) {}
}
