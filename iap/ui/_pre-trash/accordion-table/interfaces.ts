
interface Options {
    color?: string;
}
interface TableOptions extends Options {

}
interface SectionOptions extends Options {

}
interface CellOptions extends Options {

}
export interface RowOptions extends Options {

}
interface TblCell {
    value: number|string;
    type: string;
    options: CellOptions;
}
export interface TblRow {
    meta: {label: string}; // Array<{name: string}>
    data: {[s: string]: TblCell}; // cells: Array<TblCell>;
    children?: Array<TblRow>;
    options?: RowOptions;
}
export interface TblSection {
    rows: Array<TblRow>;
    options?: SectionOptions;
}
export interface ITable {
    head: TblSection;
    body: TblSection;
    options?: TableOptions;
}
