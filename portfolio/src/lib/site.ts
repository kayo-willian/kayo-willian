
import catalog from '../../content/catalog.json';
import projectData from '../../content/projects.json';
import details from '../../content/project-details.json';
import quotes from '../../content/quotes.json';
export { catalog, quotes };
export type Lang = 'en' | 'pt';
export const t = (lang: Lang, en: string, pt: string) => lang === 'en' ? en : pt;
export const root = import.meta.env.BASE_URL.replace(/\/$/, '') + '/';
export const url = (lang: Lang, path = '') => root + (lang === 'pt' ? 'pt-br/' : '') + (path ? path.replace(/\/$/, '') + '/' : '');
export const social = [
  {label:'GitHub',href:'https://github.com/kayo-willian'},
  {label:'LinkedIn',href:'https://www.linkedin.com/in/kayo-willian'},
  {label:'X',href:'https://x.com/kayowestlion'}
];
export const projects = projectData.projects.map(([slug,title,pt,en]) => ({
 slug,title,pt,en,details: details[slug as keyof typeof details],
 fork: ['where-the-water-goes','linux-usb-security-token'].includes(slug)
}));
export const groups = [
 {en:'Projects',pt:'Projetos',ja:'制作',id:'work',slugs:['enterprise-noc-from-scratch','soft-and-wet-homelab','oppy','usb-presence-gate','scrolllock-rgb-fix','arduino-linux-controller']},
 {en:'Labs',pt:'Laboratórios',ja:'実験',id:'labs',slugs:['linux-networking-labs','packet-tracer-labs','ubuntu-server-labs','debian-server-labs']},
 {en:'Open source contributions',pt:'Contribuições open source',ja:'自由',id:'oss',slugs:['where-the-water-goes','linux-usb-security-token']},
 {en:'Other work',pt:'Outros trabalhos',ja:'記録',id:'other',slugs:['channel-blue','kayo-willian']}
];
