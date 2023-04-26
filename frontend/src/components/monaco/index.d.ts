// import SQLSnippets from "/@/components/monaco/core/sql";

declare interface MonacoStateData {
  sqlSnippets: null | SQLSnippets,
  contentBackup: null | string,
  isSettingContent: boolean,
  jsonPath: null | string,
  options: {
    [key: string]: T;
  }
}