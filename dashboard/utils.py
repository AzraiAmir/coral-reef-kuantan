import streamlit as st
import pandas as pd

def chart_card(title, fig, df=None, height=None):
    """
    A reusable card that wraps a Plotly chart with a menu for downloading PNG, CSV, and Full Screen.
    """
    with st.container(border=True):
        with st.container(horizontal=True, vertical_alignment="center"):
            st.markdown(f'<div class="panel-title" style="margin: 0; padding-top: 10px;">{title}</div>', unsafe_allow_html=True)
            
            st.space("stretch")
            
            with st.popover("⚙", help="Chart Options"):
                img_bytes = fig.to_image(format="png", width=1200, height=800)
                st.download_button(
                    label="↓&nbsp;&nbsp;&nbsp;Download PNG",
                    data=img_bytes,
                    file_name=f"{title.lower().replace(' ', '_')}.png",
                    mime="image/png",
                    use_container_width=True,
                    key=f"png_{title}"
                )
                
                if df is not None:
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="▤&nbsp;&nbsp;&nbsp;Download CSV",
                        data=csv,
                        file_name=f"{title.lower().replace(' ', '_')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key=f"csv_{title}"
                    )
                
                if st.button("⤢&nbsp;&nbsp;&nbsp;Toggle Full Screen", use_container_width=True, key=f"fs_{title}"):
                    st.session_state[f"fullscreen_{title}"] = not st.session_state.get(f"fullscreen_{title}", False)

        is_fullscreen = st.session_state.get(f"fullscreen_{title}", False)
        fig_height = 800 if is_fullscreen else (height if height else 400)
        
        fig.update_layout(height=fig_height)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})