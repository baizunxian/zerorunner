// 接口类型声明

// 布局配置

export interface ThemeConfigState {
  themeConfig: {
    isDrawer: boolean;
    primary: string;
    topBar: string;
    topBarColor: string;
    isTopBarColorGradual: boolean;
    menuBar: string;
    menuBarColor: string;
    isMenuBarColorGradual: boolean;
    columnsMenuBar: string;
    columnsMenuBarColor: string;
    isColumnsMenuBarColorGradual: boolean;
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
    globalComponentSize: string;
  };
}

// 路由列表
export interface RoutesListState {
  routesList: object[];
  isColumnsMenuHover: Boolean;
  isColumnsNavHover: Boolean;
}

// 路由缓存列表
export interface KeepAliveNamesState {
  keepAliveNames: string[];
}

// TagsView 路由列表
export interface TagsViewRoutesState {
  tagsViewRoutes: object[];
  isTagsViewCurrenFull: Boolean;
}

// 用户信息
export interface UserInfosState {
  userInfos: {
    id: any;
    authBtnList: string[];
    photo: string;
    roles: string[];
    menus: object[];
    time: number;
    username: string;
    nickname: string;
    user_type: any;
  };
}

// 后端返回原始路由(未处理时)
export interface RequestOldRoutesState {
  requestOldRoutes: object[];
}

// lookup
export interface LookUpState {
  lookup: object
}

// lookup
export interface EnvState {
  envId: number | null
}

// 主接口(顶级类型声明)
export interface RootStateTypes {
  themeConfig: ThemeConfigState;
  routesList: RoutesListState;
  keepAliveNames: KeepAliveNamesState;
  tagsViewRoutes: TagsViewRoutesState;
  userInfos: UserInfosState;
  lookup: any;
  envId: number | null;
  requestOldRoutes: RequestOldRoutesState;
}
