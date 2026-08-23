/**
 * Build a URL that respects the configured `base` path.
 *
 * The site is served from https://thetilakraj.github.io/portfolio/, so a bare
 * "/about" would 404. Every internal href and asset path must go through here.
 *
 *   url()                  -> "/portfolio/"
 *   url('/work')           -> "/portfolio/work"
 *   url('resume.pdf')      -> "/portfolio/resume.pdf"
 */
const BASE = import.meta.env.BASE_URL.replace(/\/+$/, '');

export function url(path: string = '/'): string {
  const suffix = path.startsWith('/') ? path : `/${path}`;
  return `${BASE}${suffix}`;
}

/** True when `href` is the current page, for nav active states. */
export function isCurrent(href: string, pathname: string): boolean {
  const a = url(href).replace(/\/+$/, '');
  const b = pathname.replace(/\/+$/, '');
  return a === b || (a !== BASE && b.startsWith(`${a}/`));
}
