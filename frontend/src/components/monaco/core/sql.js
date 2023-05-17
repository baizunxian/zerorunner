/* jshint esversion: 8 */

// import keywords from './keywords';

export default class Snippets {
  constructor(monaco, onInputTableColumn, onInputTableAila, dbSchema = [{
    dbName: '',
    tables: [
      {
        tblName: '',
        tableColumns: []
      }
    ]
  }]) {
    this.SORT_TEXT = {
      Database: '0',
      Table: '1',
      Column: '2',
      Keyword: '3'
    };
    this.customKeywords = [];
    // this.dbKeywords = [...keywords, ...customKeywords]
    this.dbKeywords = [];
    this.dbSchema = dbSchema;
    this.monaco = monaco;
    this.getKeywordSuggest = this.getKeywordSuggest.bind(this);
    this.getTableSuggest = this.getTableSuggest.bind(this);
    this.getTableColumnSuggest = this.getTableColumnSuggest.bind(this);
    // 字段联想callback
    this.onInputTableColumn = onInputTableColumn;
    // <别名>.<字段>联想callback
    this.onInputTableAila = onInputTableAila;
  }

  /**
   * 动态设置数据库表&&数据库字段
   * @param {*} dbSchema 数据库schema
   * @example [{ dbName: '', tables: [{ tblName: '', tableColumns: [] }] }]
   */
  setDbSchema(dbSchema) {
    this.dbSchema = dbSchema;
  }

  /**
   * monaco提示方法
   * @param {*} model
   * @param {*} position
   */
  async provideCompletionItems(model, position) {
    const {lineNumber, column} = position;
    // 光标前文本
    const textBeforePointer = model.getValueInRange({
      startLineNumber: lineNumber,
      startColumn: 0,
      endLineNumber: lineNumber,
      endColumn: column
    });
    console.log("光标前文本", textBeforePointer);
    const textBeforePointerMulti = model.getValueInRange({
      startLineNumber: 1,
      startColumn: 0,
      endLineNumber: lineNumber,
      endColumn: column
    });
    // 光标后文本
    // const textAfterPointer = model.getValueInRange({
    //   startLineNumber: lineNumber,
    //   startColumn: column,
    //   endLineNumber: lineNumber,
    //   endColumn: model.getLineMaxColumn(model.getLineCount())
    // })
    const textAfterPointerMulti = model.getValueInRange({
      startLineNumber: lineNumber,
      startColumn: column,
      endLineNumber: model.getLineCount(),
      endColumn: model.getLineMaxColumn(model.getLineCount())
    });
    // const nextTokens = textAfterPointer.trim().split(/\s+/)
    // const nextToken = nextTokens[0].toLowerCase()
    const tokens = textBeforePointer.trim().split(/\s+/);
    const lastToken = tokens[tokens.length - 1].toLowerCase();
    console.log("lastToken", lastToken);
    // 数据库名联想
    if (lastToken === 'database') {
      return {
        suggestions: this.getDataBaseSuggest()
      };
      // <库名>.<表名> || <别名>.<字段>
    } else if (lastToken.endsWith('.')) {
      // 去掉点后的字符串
      const tokenNoDot = lastToken.slice(0, lastToken.length - 1);
      if (this.dbSchema.find(db => db.dbName === tokenNoDot.replace(/^.*,/g, ''))) {
        // <库名>.<表名>联想
        console.log("库名.表名 联想", lastToken);
        return {
          suggestions: [...this.getTableSuggestByDbName(tokenNoDot.replace(/^.*,/g, ''))]
        };
      } else if (this.getTableNameAndTableAlia(textBeforePointerMulti.split(';')[textBeforePointerMulti.split(';').length - 1] + textAfterPointerMulti.split(';')[0])) {
        const tableInfoList = this.getTableNameAndTableAlia(textBeforePointerMulti.split(';')[textBeforePointerMulti.split(';').length - 1] + textAfterPointerMulti.split(';')[0]);
        const currentTable = tableInfoList.find(item => item.tableAlia === tokenNoDot.replace(/^.*,/g, '') || item.tableName === tokenNoDot.replace(/^.*,/g, ''));
        console.log("currentTable", currentTable);
        // <别名>.<字段>联想
        if (currentTable && currentTable.tableName) {
          console.log("别名.字段 联想", lastToken);
          console.log("别名.字段 联想", await this.getTableColumnSuggestByTableAlia(currentTable.tableName));
          return {
            suggestions: await this.getTableColumnSuggestByTableAlia(currentTable.tableName)
          };
        } else {
          console.log("别名.字段 联想  -> 空", lastToken);
          return {
            suggestions: []
          };
        }
      } else {
        return {
          suggestions: []
        };
      }
      // 库名联想
    } else if (lastToken === 'from' || lastToken === 'join' || /(from|join)\s+.*?\s?,\s*$/.test(textBeforePointer.replace(/.*?\(/gm, '').toLowerCase())) {
      // const tables = this.getTableSuggest()
      const databases = this.getDataBaseSuggest();
      console.log("库名联想", lastToken, databases);
      return {
        suggestions: databases
      };
      // 字段联想
    } else if (['select', 'where', 'order by', 'group by', 'by', 'and', 'or', 'having', 'distinct', 'on'].includes(lastToken.replace(/.*?\(/g, '')) || (lastToken.endsWith('.') && !this.dbSchema.find(db => `${db.dbName}.` === lastToken)) || /(select|where|order by|group by|by|and|or|having|distinct|on)\s+.*?\s?,\s*$/.test(textBeforePointer.toLowerCase())) {
      console.log("字段联想", lastToken);
      return {suggestions : []}
      // return {
      //   suggestions: await this.getTableColumnSuggest()
      // };
      // 自定义字段联想
    } else if (this.customKeywords.toString().includes(lastToken)) {
      console.log("自定义字段联想", lastToken);
      return {
        suggestions: this.getCustomSuggest(lastToken.startsWith('$'))
      };
      // 默认联想
    } else {
      return {
        suggestions: [...this.getDataBaseSuggest(), ...this.getTableSuggest(), ...this.getKeywordSuggest()]
      };
    }
  }

  /**
   * 获取自定义联想建议
   */
  getCustomSuggest(startsWith$) {
    return this.customKeywords.map(keyword => ({
      label: keyword,
      kind: this.monaco.languages.CompletionItemKind.Keyword,
      detail: '',
      sortText: this.SORT_TEXT.Keyword, // Fix插入两个$符号
      insertText: startsWith$ ? keyword.slice(1) : keyword
    }));
  }

  /**
   * 获取所有字段
   */
  getAllTableColumn() {
    const tableColumns = [];
    this.dbSchema.forEach(db => {
      db.tables.forEach(table => {
        table.tableColumns.forEach(field => {
          tableColumns.push({
            label: field.columnName ? field.columnName : '',
            kind: this.monaco.languages.CompletionItemKind.Module,
            detail: `<字段><${field.columnType}>`,
            sortText: this.SORT_TEXT.Column,
            insertText: field.columnName ? field.columnName : ''
          });
        });
      });
    });
    return tableColumns;
  }

  /**
   * 获取数据库库名联想建议
   */
  getDataBaseSuggest() {
    return this.dbSchema.map(db => {
      return {
        label: db.dbName ? db.dbName : '',
        kind: this.monaco.languages.CompletionItemKind.Class,
        detail: `<数据库>`,
        sortText: this.SORT_TEXT.Database,
        insertText: db.dbName ? db.dbName : ''
      };
    });
  }

  /**
   * 获取关键字联想建议
   * @param {*} keyword
   */
  getKeywordSuggest() {
    return this.dbKeywords.map(keyword => ({
      label: keyword,
      kind: this.monaco.languages.CompletionItemKind.Keyword,
      detail: '<关键字>',
      sortText: this.SORT_TEXT.Keyword, // Fix插入两个$符号
      insertText: keyword.startsWith('$') ? keyword.slice(1) : keyword
    }));
  }

  /**
   * 获取数据库表名建议
   */
  getTableSuggest() {
    const tables = []
    this.dbSchema.forEach(db => {
      db.tables.forEach(table => {
        tables.push({
          label: table.tblName ? table.tblName : '',
          kind: this.monaco.languages.CompletionItemKind.Struct,
          detail: `<表> ${db.dbName} ${table.tblComment ? table.tblComment : ''}`,
          sortText: this.SORT_TEXT.Table,
          insertText: table.tblName ? table.tblName : '',
          documentation: table.tblComment ? table.tblComment : ''
        });
      });
    });
    return tables;
  }

  getTableSuggestByDbName(dbName) {
    const currentDb = this.dbSchema.find(db => db.dbName === dbName)
    console.log("getTableSuggestByDbName", currentDb, dbName);
    const tables = [];
    if (currentDb) {
      currentDb.tables.forEach(table => {
        tables.push({
          label: table.tblName ? table.tblName : '',
          kind: this.monaco.languages.CompletionItemKind.Struct,
          detail: `<表> ${currentDb.dbName} ${table.tblComment ? table.tblComment : ''}`,
          sortText: this.SORT_TEXT.Table,
          insertText: table.tblName ? table.tblName : '',
          documentation: table.tblComment ? table.tblComment : ''
        });
      });
    }
    return tables;
  }

  /**
   * 获取所有表字段
   * @param {*} table
   * @param {*} column
   */
  async getTableColumnSuggest() {
    const defaultFields = [];
    this.dbSchema.forEach(db => {
      db.tables.forEach(table => {
        table.tableColumns && table.tableColumns.forEach(field => {
          defaultFields.push({
            label: field.columnName ? `${table.tblName}.${field.columnName}` : '',
            kind: this.monaco.languages.CompletionItemKind.Field,
            detail: `<字段> ${field.commentName ? field.commentName : ''} <${field.columnType}>`,
            sortText: this.SORT_TEXT.Column,
            insertText: field.columnName ? field.columnName : '',
            documentation: {
              value: `
  ### 数据库: ${field.dbName}
  ### 表: ${field.tblName}
  ### 注释: ${field.commentName ? field.commentName : ''}
              `
            }
          });
        });
      });
    });
    const asyncFields = [];
    if (typeof this.onInputTableColumn === 'function') {
      const fileds = await this.onInputTableColumn();
      fileds.forEach(field => {
        asyncFields.push({
          label: field.columnName ? field.columnName : '',
          kind: this.monaco.languages.CompletionItemKind.Field,
          detail: `<字段> ${field.commentName ? field.commentName : ''} <${field.columnType}>`,
          sortText: this.SORT_TEXT.Column,
          insertText: field.columnName ? field.columnName : '',
          documentation: {
            value: `
### 数据库: ${field.dbName}
### 表: ${field.tblName}
### 注释: ${field.commentName ? field.commentName : ''}
            `
          }
        });
      });
    }
    return [...defaultFields, ...asyncFields];
  }

  /**
   * 根据别名获取所有表字段
   * @param {*} table
   * @param {*} column
   */
  async getTableColumnSuggestByTableAlia(tableName) {
    const defaultFields = [];
    this.dbSchema.forEach(db => {
      db.tables.forEach(table => {
        if (tableName === table.tblName) {
          table.tableColumns && table.tableColumns.forEach(field => {
            defaultFields.push({
              label: field.columnName ? field.columnName : '',
              kind: this.monaco.languages.CompletionItemKind.Field,
              detail: `<字段> ${field.commentName ? field.commentName : ''} <${field.columnType}>`,
              sortText: this.SORT_TEXT.Column,
              insertText: field.columnName ? field.columnName : '',
              documentation: {
                value: `
  ### 数据库: ${field.dbName}
  ### 表: ${field.tblName}
  ### 注释: ${field.commentName ? field.commentName : ''}
              `
              }
            });
          });

        }

      });
    });
    const asyncFields = [];
    if (typeof this.onInputTableAila === 'function') {
      const fileds = await this.onInputTableAila(tableName);
      fileds.forEach(field => {
        asyncFields.push({
          label: field.columnName ? field.columnName : '',
          kind: this.monaco.languages.CompletionItemKind.Field,
          detail: `<字段> ${field.commentName ? field.commentName : ''} <${field.columnType}>`,
          sortText: this.SORT_TEXT.Column,
          insertText: field.columnName ? field.columnName : '',
          documentation: {
            value: `
### 数据库: ${field.dbName}
### 表: ${field.tblName}
### 注释: ${field.commentName ? field.commentName : ''}
            `
          }
        });
      });
    }
    return [...defaultFields, ...asyncFields];
  }

  /**
   * 获取sql中所有的表名和别名
   * @param {*} sqlText SQL字符串
   */
  getTableNameAndTableAlia(sqlText) {
    const regTableAliaFrom = /(^|(\s+))from\s+([^\s]+(\s+||(\s+as\s+))[^\s]+(\s+|,)\s*)+(\s+(where|left|right|full|join|inner|union))?/ig;
    const regTableAliaJoin = /(^|(\s+))join\s+([^\s]+)\s+(as\s+)?([^\s]+)\s+on/ig;
    const regTableAliaFromList = sqlText.match(regTableAliaFrom) ? sqlText.match(regTableAliaFrom) : [];
    const regTableAliaJoinList = sqlText.match(regTableAliaJoin) ? sqlText.match(regTableAliaJoin) : [];
    const strList = [...regTableAliaFromList.map(item => item.replace(/(^|(\s+))from\s+/ig, '').replace(/\s+(where|left|right|full|join|inner|union)((\s+.*?$)|$)/ig, '').replace(/\s+as\s+/gi, ' ').trim()), ...regTableAliaJoinList.map(item => item.replace(/(^|(\s+))join\s+/ig, '').replace(/\s+on((\s+.*?$)|$)/, '').replace(/\s+as\s+/gi, ' ').trim())];
    const tableList = [];
    strList.map(tableAndAlia => {
      tableAndAlia.split(',').forEach(item => {
        const tableName = item.trim().split(/\s+/)[0];
        const tableAlia = item.trim().split(/\s+/)[1];
        tableList.push({
          tableName, tableAlia
        });
      });
    });
    console.log("sqlText", sqlText);
    console.log("strList", strList);
    console.log("regTableAliaFromList", regTableAliaFromList);
    console.log("regTableAliaJoinList", regTableAliaJoinList);
    console.log("regTableAliaFromList", regTableAliaFromList);
    console.log("regTableAliaJoinList", regTableAliaJoinList);
    console.log("获取sql中所有的表名和别名", tableList);
    return tableList;
  }
}