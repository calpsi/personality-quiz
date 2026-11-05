'use client';

const common = {viewBox:'0 0 360 210', role:'img'};

export default function OddityGraphic({kind}) {
  if (kind === 'clock') return <svg {...common} aria-label="A brass clock whose hands turn backwards" className="oddity-graphic clock-graphic">
    <path className="oddity-halo" d="M80 106c0-58 47-94 100-94s100 36 100 94-47 92-100 92S80 164 80 106Z"/>
    <path className="oddity-wood" d="M94 63 115 32h130l22 31-13 122H106Z"/>
    <circle className="oddity-paper" cx="180" cy="108" r="58"/>
    <circle className="oddity-brass" cx="180" cy="108" r="50"/>
    {[0,1,2,3,4,5,6,7,8,9,10,11].map(i=><line key={i} className="clock-mark" x1="180" y1="63" x2="180" y2="70" transform={`rotate(${i*30} 180 108)`}/>) }
    <g className="clock-hands"><path d="m180 108-8-35"/><path d="m180 108 31-17"/><circle cx="180" cy="108" r="5"/></g>
    <path className="oddity-spark" d="m69 63 8 8 10-16M286 89l10-4 5 11M72 150l10-2 3 10"/>
  </svg>;
  if (kind === 'drawer') return <svg {...common} aria-label="An open specimen drawer spilling small stars" className="oddity-graphic drawer-graphic">
    <ellipse className="oddity-halo" cx="180" cy="122" rx="126" ry="72"/>
    <path className="oddity-wood" d="m70 69 213 1-18 82-178 5Z"/><path className="oddity-brass" d="m88 87 164-1-11 53-143 4Z"/>
    <path className="drawer-dark" d="m100 92 145-1-14 39-121 4Z"/>
    <g className="drawer-stars"><path d="m143 103 5 10 11 2-8 8 2 12-10-6-10 6 2-12-8-8 11-2Z"/><path d="m190 89 4 8 9 1-7 7 2 9-8-5-8 5 2-9-7-7 9-1Z"/><path d="m222 110 3 6 7 1-5 5 1 7-6-4-6 4 1-7-5-5 7-1Z"/></g>
    <path className="oddity-paper drawer-front" d="m86 152 179-5 20 29-215 5Z"/><circle className="oddity-brass" cx="177" cy="164" r="8"/>
    <g className="floating-star"><path d="m123 44 5 10 11 2-8 8 2 11-10-5-10 5 2-11-8-8 11-2Z"/></g><circle className="mote mote-a" cx="231" cy="48" r="5"/><circle className="mote mote-b" cx="270" cy="105" r="3"/>
  </svg>;
  if (kind === 'labels') return <svg {...common} aria-label="Museum labels drifting away from their strings" className="oddity-graphic labels-graphic">
    <ellipse className="oddity-halo" cx="180" cy="112" rx="132" ry="75"/>
    <path className="label-string" d="M111 29c7 34 53 17 41 57s40 40 31 74M254 31c-31 25-8 46-34 64s-20 39-3 61"/>
    <g className="tag tag-a"><path className="oddity-paper" d="m62 55 93-16 12 53-94 17Z"/><circle cx="151" cy="52" r="4"/><path d="M83 72h55M80 84h40"/></g>
    <g className="tag tag-b"><path className="oddity-paper" d="m193 85 102 12-7 57-102-12Z"/><circle cx="205" cy="99" r="4"/><path d="m212 114 58 7m-60 8 41 5"/></g>
    <path className="oddity-spark" d="m77 142 9 7 8-10m77-115 5 10 11-5"/>
  </svg>;
  if (kind === 'meteorite') return <svg {...common} aria-label="A faceted meteorite hovering over its empty stand" className="oddity-graphic meteorite-graphic">
    <ellipse className="oddity-halo" cx="180" cy="105" rx="118" ry="74"/>
    <g className="meteor"><path className="rock-a" d="m121 89 38-47 61 9 31 53-31 48-71 4-38-36Z"/><path className="rock-b" d="m159 42 19 53-57-6Zm19 53 73 9-31 48Zm0 0-29 61-38-36Zm0 0 42-44 31 53Z"/></g>
    <path className="orbit" d="M66 116c13 31 72 49 139 36s104-49 86-72-77-23-128-8"/><circle className="mote mote-a" cx="76" cy="113" r="7"/><circle className="mote mote-b" cx="287" cy="89" r="5"/>
    <path className="oddity-brass" d="m121 183 26-20h66l27 20Z"/>
  </svg>;
  return <svg {...common} aria-label="Pressed leaves wandering out of their frame" className="oddity-graphic leaves-graphic">
    <ellipse className="oddity-halo" cx="180" cy="110" rx="127" ry="76"/>
    <rect className="oddity-wood" x="96" y="27" width="168" height="154" rx="3"/><rect className="oddity-paper" x="109" y="40" width="142" height="128"/>
    <path className="stem" d="M177 147c4-37-8-65-28-91m28 91c18-28 24-55 18-80"/>
    <g className="frame-leaves"><ellipse cx="148" cy="75" rx="13" ry="25" transform="rotate(-40 148 75)"/><ellipse cx="169" cy="99" rx="13" ry="25" transform="rotate(42 169 99)"/><ellipse cx="195" cy="84" rx="13" ry="25" transform="rotate(38 195 84)"/></g>
    <g className="wandering-leaf"><ellipse cx="281" cy="56" rx="13" ry="27" transform="rotate(48 281 56)"/><path d="m266 71 31-30"/></g><g className="wandering-leaf second"><ellipse cx="69" cy="131" rx="12" ry="25" transform="rotate(-55 69 131)"/><path d="m55 142 29-23"/></g>
  </svg>;
}
