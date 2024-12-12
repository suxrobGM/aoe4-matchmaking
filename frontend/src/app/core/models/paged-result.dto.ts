export interface PagedResult<T = unknown> {
  data: T[];
  error?: string | null;
  success: boolean;
  pageIndex: number;
  pageSize: number;
  pagesCount: number;
}
