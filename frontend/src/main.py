import asyncio
import httpx
import streamlit as st

from src.config.base import settings


async def fetch_packages(page: int):
    async with httpx.AsyncClient() as client:
        result = await client.get(
            f"http://{settings.server_address}/api/v1/packages/?page={page}"
        )

    return result.json()


async def fetch_dependency(dependency: str):
    async with httpx.AsyncClient() as client:
        result = await client.get(
            f"http://{settings.server_address}/api/v1/packages/{dependency}"
        )

    return result.json()


async def dashboard():
    page = int(st.query_params.get("page", 1))
    packages = await fetch_packages(page)

    cols = st.columns(5)
    with cols[0]:
        st.subheader(f"📖 Page: {packages['page']}")
    with cols[4]:
        st.subheader(f"🔎 Total Packages: {packages['total']}")

    cols = st.columns(11)
    with cols[4]:
        st.write(
            f"""
            <a href="?page={max(1, packages["page"] - 1)}" target="_self">
                <button>
                    《  Pre
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )

    with cols[6]:
        st.write(
            f"""
            <a href="?page={min(packages["pages"], packages["page"] + 1)}" target="_self">
                <button>
                    Next  》
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )

    for item in packages["items"]:
        with st.expander(f"⭕ Package #{item['id']}: **{item['name']}**"):
            for key, value in item.items():
                if key in ["id", "name"]:
                    continue

                if not isinstance(value, list):
                    st.write(f"🔻 **{key.replace('_', ' ').title()}**: {value}")
                else:
                    if value:
                        st.write(f"🔻 **{key.replace('_', ' ').title()}**:")
                        for sub_item in value:
                            if sub_item.get("dependency_package"):
                                title = sub_item.get("dependency_package")
                            else:
                                title = sub_item.get("dependent_package")
                            url = f"?dependency={sub_item["url"].split("/")[-1]}"
                            st.markdown(
                                f'🔗 <a href="{url}" target="_self">{title}</a>',
                                unsafe_allow_html=True,
                            )


async def dependency():
    st.write(
        """
        <a target="_self" href="http://localhost:8501/?page=1">
            <button>
                Home
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

    item = await fetch_dependency(st.query_params["dependency"])

    with st.expander(f"⭕ Package {item['id']}: **{item['name']}**", expanded=True):
        for key, value in item.items():
            if key in ["id", "name"]:
                continue

            if not isinstance(value, list):
                st.write(f"🔸 **{key.replace('_', ' ').title()}**: {value}")
            else:
                if value:
                    st.write(f"🔸 **{key.replace('_', ' ').title()}**:")
                    for sub_item in value:
                        if sub_item.get("dependency_package"):
                            title = sub_item.get("dependency_package")
                        else:
                            title = sub_item.get("dependent_package")
                        url = f"?dependency={sub_item["url"].split("/")[-1]}"
                        st.markdown(
                            f'🔗 <a href="{url}" target="_self">{title}</a>',
                            unsafe_allow_html=True,
                        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="dpkg Profiler Dashboard",
        page_icon="👀",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/ko-sangari/dpkg-profiler",
            "Report a bug": "https://github.com/ko-sangari/dpkg-profiler",
            "About": "A FastAPI/Streamlit app to profile the system's dpkg packages.",
        },
    )
    st.markdown(
        """
    <style>
        /* Streamlit class name of the div that holds the expander's title*/
        .st-emotion-cache-sh2krr p {
            font-size: 20px;
        }

        /* Button CSS*/
        .st-emotion-cache-cnbvxy a button {
            appearance: button;
            background-color: #1899D6;
            border: solid transparent;
            border-radius: 16px;
            border-width: 0 0 4px;
            box-sizing: border-box;
            color: #FFFFFF;
            cursor: pointer;
            display: inline-block;
            font-family: din-round,sans-serif;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: .8px;
            line-height: 20px;
            margin: 0;
            margin-bottom: 20px;
            outline: none;
            overflow: visible;
            padding: 13px 16px;
            text-align: center;
            text-transform: uppercase;
            touch-action: manipulation;
            transform: translateZ(0);
            transition: filter .2s;
            user-select: none;
            -webkit-user-select: none;
            vertical-align: middle;
            white-space: nowrap;
            width: 100px;
        }

        .st-emotion-cache-cnbvxy a button:after {
            background-clip: padding-box;
            background-color: #1CB0F6;
            border: solid transparent;
            border-radius: 16px;
            border-width: 0 0 4px;
            bottom: -4px;
            content: "";
            left: 0;
            position: absolute;
            right: 0;
            top: 0;
            z-index: -1;
        }

        .st-emotion-cache-cnbvxy a button:main,
        .st-emotion-cache-cnbvxy a button:focus {
            user-select: auto;
        }

        .st-emotion-cache-cnbvxy a button:hover:not(:disabled) {
            filter: brightness(1.1);
            -webkit-filter: brightness(1.1);
        }

        .st-emotion-cache-cnbvxy a button:disabled {
            cursor: auto;
        }

        .st-emotion-cache-cnbvxy a button:active {
            border-width: 4px 0 0;
            background: none;
        }                
    </style>
    """,
        unsafe_allow_html=True,
    )

    if "dependency" in st.query_params:
        asyncio.run(dependency())
    else:
        asyncio.run(dashboard())
