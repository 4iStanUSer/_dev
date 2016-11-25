export class TimePeriodInput { // Interface
    start: string;
    end: string;
    scale: string;
    //mid: string; // TODO Optional param -
}

export class TimePeriodModel { // TODO Post TimeLabel Object
    constructor(
        public start: string,
        public end: string,
        public scale: string,
        public mid: string = null
    ) {}
}
