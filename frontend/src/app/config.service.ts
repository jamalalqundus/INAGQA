/**
 * Name:     config.service.ts
 * Author:   ssa
 * 
 * Description: Service that makes the environment variables from assets/config.json 
 *  accessible to other services in the application.
 * 
 * 
*/

import { Injectable, APP_INITIALIZER } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class ConfigService {

    configUrl = 'assets/config.json';
    private config: Object;

    constructor(private http: HttpClient) { }

    getConfig() { return this.http.get(this.configUrl); }      

    loadConfig() {
        return new Promise((resolve, reject) => { 
            this.getConfig()
            .subscribe((data: Object) => {
                this.config = JSON.parse(JSON.stringify(data));
                resolve(true);
            });
        })
    }

    getKey(key: any){
        return this.config[key];
    }
}

export function ConfigFactory(config: ConfigService) {
    return () => config.loadConfig();
}

export function init() {
    return {
        provide: APP_INITIALIZER,
        useFactory: ConfigFactory,
        deps: [ConfigService],
        multi: true
    }
}

const ConfigModule = {
    init: init
}

export { ConfigModule };
