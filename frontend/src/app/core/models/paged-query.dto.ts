export interface PagedQuery {
  page: number;
  pageSize: number;
  orderBy?: string;
  filter?: string;
}
