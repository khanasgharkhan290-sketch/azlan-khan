        hours_per_week = st.number_input(
            "Study hours per week *",
            min_value=1,
            max_value=80,
            value=8,
            step=1,
            help="Choose the number of hours you can consistently protect each week.",
        )
        learning_goal = st.text_input(
            "Learning goal (optional)",
            placeholder="e.g., Build and deploy a portfolio project",
            max_chars=250,
        )
    submitted = st.form_submit_button(
        "✨ Generate my learning roadmap",
        type="primary",
        use_container_width=True,
    )

if submitted:
    if not domain.strip():
        st.error("Please enter a learning domain before generating your roadmap.")
    elif len(domain.strip()) < 2:
        st.error("Please enter a more specific learning domain (at least 2 characters).")
    elif re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", domain):
        st.error("The learning domain contains unsupported control characters.")
    else:
        with st.spinner("Designing your personalized learning roadmap…"):
            try:
                roadmap = generate_roadmap(
                    domain=domain.strip(),
                    level=level,
                    duration=duration,
                    hours_per_week=int(hours_per_week),
                    learning_goal=learning_goal,
                )
                st.session_state["roadmap"] = roadmap
                st.session_state["roadmap_inputs"] = {
                    "domain": domain.strip(),
                    "level": level,
                    "duration": duration,
                    "hours_per_week": int(hours_per_week),
                    "learning_goal": learning_goal,
                }
                st.success("Your learning roadmap is ready!")
            except ValueError as exc:
                st.error(str(exc))
            except AuthenticationError:
                st.error(
                    "Groq rejected the API key. Check that GROQ_API_KEY is correct "
                    "and active, then try again."
                )
            except RateLimitError:
                st.warning(
                    "The Groq API rate limit or quota has been reached. Wait a little "
                    "while, check your Groq usage limits, and try again."
                )
            except APIConnectionError:
                st.error(
                    "Could not connect to Groq. Check your internet connection and "
                    "Groq service status, then retry."
                )
            except BadRequestError as exc:
                st.error(
                    "Groq rejected the request. The selected model may be unavailable "
                    "or the request may be too large. Details: " + str(exc)
                )
            except APIStatusError as exc:
                st.error(
                    f"Groq returned an API error (HTTP {exc.status_code}). "
                    "Please retry later. If it continues, check the Groq dashboard."
                )
            except Exception as exc:
                st.error(
                    "An unexpected error occurred while generating the roadmap. "
                    f"Details: {exc}"
                )

# ---------------------------------------------------------------------
# Roadmap output and download
# ---------------------------------------------------------------------
if st.session_state.get("roadmap"):
    saved = st.session_state["roadmap_inputs"]
    st.markdown("---")
    st.subheader("📚 Your personalized roadmap")
    st.caption(
        f"{saved['domain']} · {saved['level']} · {saved['duration']} · "
        f"{saved['hours_per_week']} hours/week"
    )
    st.markdown(st.session_state["roadmap"])

    download_content = make_download_text(
        roadmap=st.session_state["roadmap"],
        domain=saved["domain"],
        level=saved["level"],
        duration=saved["duration"],
        hours_per_week=saved["hours_per_week"],
        goal=saved["learning_goal"],
    )
    safe_domain = re.sub(r"[^A-Za-z0-9_-]+", "_", saved["domain"]).strip("_")
    filename = f"{safe_domain or 'learning'}_roadmap.md"
    st.download_button(
        "⬇️ Download roadmap (Markdown)",
        data=download_content,
        file_name=filename,
        mime="text/markdown",
        use_container_width=True,
    )
    st.caption("Markdown files can be opened in any text editor or converted to PDF.")
else:
    st.info("Your generated roadmap will appear here. Start by completing the form above.")

st.markdown("---")
st.markdown(
    '<p class="small-note">Built with Streamlit and Groq. Learning resources and '
    'career suggestions are AI-generated; verify important details and adapt the plan '
    'to your circumstances.</p>',
    unsafe_allow_html=True,
)
