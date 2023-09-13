declare type data<T = any> = {
	code: number;
	data: T;
	message: string;
	type?: string;
	[key: string]: T;
};


declare type col<T = any> = {
	title: string;
	key: string;
	width?: string | number;
	height?: string | number;
	type?: string | number;
	colWidth?: string;
	lookupCode?: string;
	dateFormat?: string;
	[key: string]: T;
};

declare type columns<T = any> = {
	col: Array<col<T>>;
}