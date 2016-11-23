import { Injectable } from '@angular/core';

interface ICallable {
    obj: Object;
    meth: string;
}

@Injectable()
export class MachineGunnerService {
    private storage: { [s: string]: Array<ICallable>; } = {};
    private notCatched: { [s: string]: Array<Object>; } = {};

    public listen(event: string, callable: ICallable) {
        if (callable.obj && callable.meth &&
            callable.meth in callable.obj &&
            typeof callable.obj[callable.meth] == "function") {
            if (!(event in this.storage)) {
                this.storage[event] = [];
            }
            if (this.storage[event].indexOf(callable) == -1) {
                this.storage[event].push(callable);
                console.debug('Add listener for event "' + event + '"');
            } else {
                console.warn('Such callable exists already');
                console.info(callable);
            }
            // if there are uncatched events. Fire them and clear the variable
            if (this.notCatched[event]) {
                for (let i = 0; i < this.notCatched[event].length; i++) {
                    this.fire(event, this.notCatched[event][i]);
                }
                this.notCatched[event] = [];
            }
        }
    }
    public fire(event: string, data: Object) {
        if (event && event.length) {
            if (event in this.storage) {
                for (let i = 0; i < this.storage[event].length; i++) {
                    let c = this.storage[event][i];
                    console.debug('Start event firing "' + event + '"');
                    c.obj[c.meth](data);
                }
            } else {
                if (!(event in this.notCatched)) {
                    this.notCatched[event] = [];
                }
                this.notCatched[event].push(data);
            }
        }
    }
    public drop() {
        this.storage = {};
        this.notCatched = {};
    }
}
