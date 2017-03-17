import { ScenarioModel, ScenarioDetailsModel } from './scenario.model';


export const ScenarioDetails: ScenarioDetailsModel = {
    modify_date: "2017-03-03 11:49:42.174458",
    selectors: [
        {key: 'region', values: ['United States', 'Texas', 'Dallas']},
        {key: 'channel', values: ['United States', 'Dallas']},
        {key: 'type', values: ['United States', 'Texas', 'Dallas']},
        {key: 'brand', values: ['United States', 'Texas']}
    ],
    table: [
        {drivers: 'MACROECONOMIC', growth: 'OPTIMISTIC'},
        {drivers: 'MEDIA ACTIVITY', growth: '-0.7%'},
        {drivers: 'COVERAGE', growth: '0.0%'},
        {drivers: 'PRICE-ON-VOLUME', growth: '-2.0%'},
        {drivers: 'DISTRIBUTION', growth: '-2.5%'},
        {drivers: 'RETAIL PRICE', growth: '-1.1%'},
        {drivers: 'PRODUCT LAUNCH', growth: '0.5%'},
        {drivers: 'ADDITIONAL', growth: '0.0%'},
        {drivers: 'MACROECONOMIC', growth: 'OPTIMISTIC'},
        {drivers: 'MEDIA ACTIVITY', growth: '-00.7%'},
        {drivers: 'COVERAGE', growth: '00.0%'},
        {drivers: 'PRICE-ON-VOLUME', growth: '-02.0%'},
        {drivers: 'DISTRIBUTION', growth: '-02.5%'},
        {drivers: 'RETAIL PRICE', growth: '-01.1%'},
        {drivers: 'PRODUCT LAUNCH', growth: '00.5%'},
        {drivers: 'ADDITIONAL', growth: '00.0%'}
    ],
    main_info: [
        {name: 'Growth Rate', value: '+1.3%'},
        {name: 'Sales Value', value: '3345'},
        {name: 'Long-Term', value: '+7.3%'}
    ]
};

/*
export const Scenarios: ScenarioModel[] = [
    {
        author:"user@mail.com", criteria:"USA-iPhone-Main", description:"Dynamics of Price Growth in USA",
        favorite:"No", id:10, modify_date:"2017-03-10 10:31:48.063205", deadline:"",
        name:"Price Growth Dynamics JJLean", scenario_permission:["copy"], shared:"No", status: "Draft"
    },
    {
        author:"user@mail.com", criteria:"USA-iPhone-Main", description:"Dynamics of Price Growth in USA",
        favorite:"No", id:11, modify_date:"2017-03-10 10:31:48.063205", deadline:"",
        name:"Price Growth Dynamics JJLean", scenario_permission:["copy"], shared:"No", status: "Draft"
    }
];
*/
