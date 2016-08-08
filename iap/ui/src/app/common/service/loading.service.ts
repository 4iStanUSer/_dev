import { Injectable } from '@angular/core';


@Injectable()
export class LoadingService { // Service || Component ?
    private queue: Array<string> = [];

    constructor() { }

    public show(id: string) {
        if (this.queue.indexOf(id) == -1) {
            this.queue.push(id);
            console.log('---show loading');
        } else {
            console.warn('process '+id+' already exists in queue!');
        }
    }
    public hide(id: string) {
        let index = this.queue.indexOf(id);
        if (index != -1) {
            this.queue.splice(index, 1);
        }
        if (this.queue.length == 0) {
            console.log('---hide loading');
        }
    }
    public getQueue(){
        return this.queue;
    }
}
