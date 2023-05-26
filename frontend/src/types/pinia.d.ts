/**
 * pinia 类型定义
 */

// 用户信息
declare interface UserInfoState<T = any> {
  userInfos: {
    id: any;
    authBtnList: string[];
    avatar: string;
    roles: string[];
    time: number;
    username: string;
    nickname: string;
    user_type: any;
    [key: string]: T;
  };
}

// 菜单信息
declare interface MenuDataState<T = any> {
  menuData: {
    [key: string]: T;
  };
}

// 路由缓存列表
declare interface KeepAliveNamesState {
  keepAliveNames: string[];
  cachedViews: string[];
}

// 后端返回原始路由(未处理时)
declare interface RequestOldRoutesState {
  requestOldRoutes: string[];
}

// TagsView 路由列表
declare interface TagsViewRoutesState<T = any> {
  tagsViewRoutes: T[];
  isTagsViewCurrenFull: Boolean;
}

// 路由列表
declare interface RoutesListState<T = any> {
  routesList: T[];
  isGet: Boolean;
  isColumnsMenuHover: Boolean;
  isColumnsNavHover: Boolean;
}

// lookup 数据字典
declare interface LookupListListState<T = any> {
  lookupList: T[];
}

// 布局配置
declare interface ThemeConfigState {
  themeConfig: {
    isDrawer: boolean;
    primary: string;
    topBar: string;
    topBarColor: string;
    isTopBarColorGradual: boolean;
    menuBar: string;
    menuBarColor: string;
    menuBarActiveColor: string;
    isMenuBarColorGradual: boolean;
    columnsMenuBar: string;
    columnsMenuBarColor: string;
    isColumnsMenuBarColorGradual: boolean;
    isColumnsMenuHoverPreload: boolean;
    isCollapse: boolean;
    isUniqueOpened: boolean;
    isFixedHeader: boolean;
    isFixedHeaderChange: boolean;
    isClassicSplitMenu: boolean;
    isLockScreen: boolean;
    lockScreenTime: number;
    isShowLogo: boolean;
    isShowLogoChange: boolean;
    isBreadcrumb: boolean;
    isTagsview: boolean;
    isBreadcrumbIcon: boolean;
    isTagsviewIcon: boolean;
    isCacheTagsView: boolean;
    isSortableTagsView: boolean;
    isShareTagsView: boolean;
    isFooter: boolean;
    isGrayscale: boolean;
    isInvert: boolean;
    isIsDark: boolean;
    isWartermark: boolean;
    wartermarkText: string;
    tagsStyle: string;
    animation: string;
    columnsAsideStyle: string;
    columnsAsideLayout: string;
    layout: string;
    isRequestRoutes: boolean;
    globalTitle: string;
    globalViceTitle: string;
    globalViceTitleMsg: string;
    globalI18n: string;
    globalComponentSize: string;
  };
}
