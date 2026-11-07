"""Pip, as one posable component.

Every page draws the same body, beak, eyes and antenna from the same code.
Only `pose` and `mood` change, so the character cannot drift between pages:
consistency is a property of the build, not a test result.

pose  -> what the wings and legs do
mood  -> eye glow and antenna tilt
"""

LOOP = 2.0

BODY, BODY_DARK = "#4A6FE8", "#3A57BE"
CREAM, GLOW, BEAK = "#FFF8E6", "#FFD23F", "#F7A23B"
INK = "#101A33"

MOOD = {   # antenna tilt, eye glow, eye squash (1 = round)
    "calm":    (0,   0.92, 1.00),
    "warm":    (-8,  1.00, 0.92),
    "curious": (-18, 1.00, 1.08),
    "quiet":   (6,   0.70, 0.78),
    "excited": (12,  1.00, 1.12),
}

# wing angles (left, right), leg offset, body tilt
POSE = {
    "stand":  ((-12, 12),   0,  0),
    "point":  ((-10, -72),  0,  4),
    "wave":   ((-74, 14),   0, -4),
    "cheer":  ((-62, 62),  -6,  0),
    "think":  ((-8, -40),   0,  6),
    "peek":   ((-16, 10),   0, -8),
    "read":   ((-46, 46),   4,  8),
    "sleep":  ((-6, 6),     8, 12),
}


def pip(x=540, y=700, scale=1.0, mood="calm", pose="stand", blink=True):
    tilt, glow, squash = MOOD.get(mood, MOOD["calm"])
    (wl, wr), legdy, lean = POSE.get(pose, POSE["stand"])
    ry = 46 * squash
    closed = "" if blink else ' style="display:none"'

    return f"""<g transform="translate({x},{y}) scale({scale})">
 <g transform="rotate({lean})">
  <g filter="url(#paint)">
   <animateTransform attributeName="transform" type="translate"
     values="0,0; 0,-10; 0,0" dur="{LOOP}s" repeatCount="indefinite" additive="sum"/>

   <ellipse cx="0" cy="14" rx="118" ry="20" fill="{INK}" opacity=".20"/>

   <!-- legs -->
   <g transform="translate(0,{legdy})">
     <path d="M-44 -18 l0 26 q0 10 -14 12 l-16 2 q-8 1 -8 -6 q0 -6 8 -8 l14 -4 l0 -22z"
           fill="{BEAK}"/>
     <path d="M44 -18 l0 26 q0 10 14 12 l16 2 q8 1 8 -6 q0 -6 -8 -8 l-14 -4 l0 -22z"
           fill="{BEAK}"/>
   </g>

   <!-- body -->
   <path d="M-112 -56 C-112 -236 112 -236 112 -56 C112 -14 62 -6 0 -6
            C-62 -6 -112 -14 -112 -56Z" fill="{BODY}"/>
   <ellipse cx="0" cy="-62" rx="66" ry="54" fill="{CREAM}"/>

   <!-- wings, one group each so a pose just rotates them -->
   <g transform="rotate({wl} -96 -120)">
     <path d="M-96 -140 C-142 -150 -150 -88 -118 -58 C-104 -46 -96 -58 -96 -74Z"
           fill="{BODY_DARK}"/>
   </g>
   <g transform="rotate({wr} 96 -120)">
     <path d="M96 -140 C142 -150 150 -88 118 -58 C104 -46 96 -58 96 -74Z"
           fill="{BODY_DARK}"/>
   </g>

   <!-- eyes -->
   <g>
     <ellipse cx="-44" cy="-148" rx="42" ry="{ry:.0f}" fill="{CREAM}"/>
     <ellipse cx="44" cy="-148" rx="42" ry="{ry:.0f}" fill="{CREAM}"/>
     <ellipse cx="-44" cy="-148" rx="27" ry="{ry*.62:.0f}" fill="{INK}"/>
     <ellipse cx="44" cy="-148" rx="27" ry="{ry*.62:.0f}" fill="{INK}"/>
     <circle cx="-34" cy="-160" r="9" fill="{CREAM}" opacity=".9"/>
     <circle cx="54" cy="-160" r="9" fill="{CREAM}" opacity=".9"/>
     <animateTransform attributeName="transform" type="scale" values="1 1;1 .08;1 1"
       dur="{LOOP}s" keyTimes="0;.9;.95" repeatCount="indefinite"{closed}/>
   </g>

   <polygon points="-18,-116 0,-92 18,-116" fill="{BEAK}"/>

   <!-- antenna -->
   <g transform="rotate({tilt} 0 -214)">
     <line x1="0" y1="-198" x2="0" y2="-256" stroke="{BODY_DARK}" stroke-width="12"
           stroke-linecap="round"/>
     <circle cx="0" cy="-266" r="15" fill="{GLOW}" opacity="{glow}">
       <animate attributeName="r" values="15;18;15" dur="{LOOP}s" repeatCount="indefinite"/>
     </circle>
   </g>
  </g>
 </g>
</g>"""
