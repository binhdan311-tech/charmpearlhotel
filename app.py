import base64
from pathlib import Path
from datetime import date, timedelta

import pandas as pd
import streamlit as st


# ============================================================
# CHARM PEARL HOTEL
# HOTEL MANAGEMENT SYSTEM
# ============================================================

st.set_page_config(
    page_title="Charm Pearl Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 1. ĐƯỜNG DẪN HÌNH ẢNH
# ============================================================

BASE_DIR = Path(__file__).parent

LOGO_PATH = BASE_DIR / "IMG_1LOGO.jpg"
BANNER_PATH = BASE_DIR / "IMG_2BANNER.jpg"
BACKGROUND_PATH = BASE_DIR / "IMG_3NENCHIM.jpg"


def image_base64(path):
    if not path.exists():
        return ""

    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode()


logo_b64 = image_base64(LOGO_PATH)
banner_b64 = image_base64(BANNER_PATH)
background_b64 = image_base64(BACKGROUND_PATH)


# ============================================================
# 2. CSS - GIAO DIỆN
# ============================================================

st.markdown(
    f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:
        wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {{
        font-family: 'Be Vietnam Pro', sans-serif;
    }}

    /* ================= APP BACKGROUND ================= */

    .stApp {{
        background:
        linear-gradient(
            rgba(245,248,250,0.94),
            rgba(245,248,250,0.94)
        ),
        url("data:image/jpeg;base64,{background_b64}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ================= SIDEBAR ================= */

    [data-testid="stSidebar"] {{
        background:
        linear-gradient(
            180deg,
            #06233d 0%,
            #0a3d5b 55%,
            #061f35 100%
        );
    }}

    [data-testid="stSidebar"] * {{
        color: white;
    }}

    /* ================= HERO ================= */

    .hero {{
        min-height: 320px;

        border-radius: 25px;

        padding: 45px;

        margin-bottom: 25px;

        background:
        linear-gradient(
            90deg,
            rgba(2,24,43,0.92),
            rgba(2,24,43,0.30)
        ),
        url("data:image/jpeg;base64,{banner_b64}");

        background-size: cover;
        background-position: center;

        box-shadow:
            0 18px 45px rgba(0,0,0,0.15);

        display: flex;
        align-items: center;
    }}

    .hero-tag {{
        display: inline-block;

        padding: 8px 15px;

        border-radius: 30px;

        background: rgba(255,255,255,0.15);

        border: 1px solid rgba(255,255,255,0.30);

        color: white;

        font-size: 11px;

        letter-spacing: 2px;

        margin-bottom: 15px;
    }}

    .hero h1 {{
        color: white;

        font-size: 44px;

        line-height: 1.08;

        margin: 0;

        font-weight: 800;
    }}

    .hero p {{
        color: #edf6fb;

        font-size: 15px;

        margin-top: 12px;
    }}

    /* ================= SECTION ================= */

    .section-title {{
        color: #082d4c;

        font-size: 23px;

        font-weight: 800;

        margin-top: 20px;

        margin-bottom: 14px;
    }}

    /* ================= CARDS ================= */

    .custom-card {{
        background: rgba(255,255,255,0.96);

        border: 1px solid #e1e9ef;

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 7px 25px rgba(8,43,70,0.07);

        margin-bottom: 15px;
    }}

    .room-card {{
        background: rgba(255,255,255,0.97);

        border: 1px solid #dfe8ef;

        border-radius: 15px;

        padding: 14px;

        text-align: center;

        min-height: 105px;

        box-shadow:
            0 4px 15px rgba(8,43,70,0.06);
    }}

    .room-number {{
        color: #082d4c;

        font-size: 20px;

        font-weight: 800;
    }}

    .room-type {{
        color: #6b7d8c;

        font-size: 11px;

        margin-top: 3px;
    }}

    .room-status {{
        font-size: 11px;

        font-weight: 700;

        margin-top: 8px;
    }}

    /* ================= INFO ================= */

    .small-text {{
        color: #657789;

        font-size: 13px;
    }}

    .price {{
        color: #08708d;

        font-weight: 800;

        font-size: 14px;
    }}

    .hotel-title {{
        color: white;

        text-align: center;

        font-size: 21px;

        font-weight: 800;

        margin-top: 8px;
    }}

    .hotel-subtitle {{
        color: rgba(255,255,255,0.7);

        text-align: center;

        font-size: 10px;

        letter-spacing: 2px;
    }}

    /* ================= BUTTON ================= */

    .stButton > button {{
        border-radius: 10px;

        font-weight: 700;
    }}

    /* ================= METRIC ================= */

    div[data-testid="stMetric"] {{
        background: rgba(255,255,255,0.96);

        border: 1px solid #e1e9ef;

        border-radius: 16px;

        padding: 15px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. DỮ LIỆU PHÒNG
# ============================================================

ROOM_PRICES = {
    "Standard": 550000,
    "Deluxe": 750000,
    "Suite": 1200000,
    "Family": 1500000
}

ROOM_STATUS = [
    "Trống",
    "Đã đặt",
    "Đang ở",
    "Đang dọn",
    "Bảo trì"
]


def create_rooms():

    rooms = []

    for floor in range(1, 6):

        for number in range(1, 11):

            room_number = f"{floor}{number:02d}"

            if number <= 4:
                room_type = "Standard"

            elif number <= 8:
                room_type = "Deluxe"

            elif number == 9:
                room_type = "Suite"

            else:
                room_type = "Family"

            # Tạo trạng thái demo
            pattern = (floor * 3 + number) % 10

            if pattern in [0, 1]:
                status = "Đang ở"

            elif pattern in [2, 3]:
                status = "Đã đặt"

            elif pattern == 4:
                status = "Đang dọn"

            elif pattern == 5:
                status = "Bảo trì"

            else:
                status = "Trống"

            rooms.append(
                [
                    room_number,
                    floor,
                    room_type,
                    ROOM_PRICES[room_type],
                    status
                ]
            )

    return pd.DataFrame(
        rooms,
        columns=[
            "Phòng",
            "Tầng",
            "Loại phòng",
            "Giá/đêm",
            "Trạng thái"
        ]
    )


# ============================================================
# 4. KHỞI TẠO SESSION
# ============================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = create_rooms()


if "bookings" not in st.session_state:

    st.session_state.bookings = pd.DataFrame(

        [
            [
                "BK0001",
                "102",
                "Nguyễn Minh Anh",
                "0901234567",
                date.today(),
                date.today() + timedelta(days=2),
                2,
                1500000,
                200000,
                1700000,
                "Đang ở"
            ],

            [
                "BK0002",
                "205",
                "Trần Hoàng Nam",
                "0912345678",
                date.today(),
                date.today() + timedelta(days=3),
                3,
                2250000,
                300000,
                2550000,
                "Đang ở"
            ],

            [
                "BK0003",
                "309",
                "Lê Ngọc Mai",
                "0923456789",
                date.today() + timedelta(days=1),
                date.today() + timedelta(days=3),
                2,
                2400000,
                0,
                2400000,
                "Đã đặt"
            ]
        ],

        columns=[
            "Mã đặt phòng",
            "Phòng",
            "Tên khách",
            "Số điện thoại",
            "Ngày nhận",
            "Ngày trả",
            "Số đêm",
            "Tiền phòng",
            "Dịch vụ",
            "Tổng tiền",
            "Trạng thái"
        ]
    )


if "services" not in st.session_state:

    st.session_state.services = pd.DataFrame(

        [
            ["DV001", "Ăn sáng", 100000],
            ["DV002", "Cà phê", 45000],
            ["DV003", "Giặt ủi", 80000],
            ["DV004", "Minibar", 60000],
            ["DV005", "Extra Bed", 200000],
            ["DV006", "Spa & Wellness", 300000],
            ["DV007", "Đưa đón sân bay", 350000],
        ],

        columns=[
            "Mã DV",
            "Tên dịch vụ",
            "Đơn giá"
        ]
    )


# ============================================================
# 5. HÀM HỖ TRỢ
# ============================================================

def money(value):
    return f"{int(value):,} VNĐ"


def status_icon(status):

    icons = {
        "Trống": "🟢",
        "Đã đặt": "🟣",
        "Đang ở": "🔵",
        "Đang dọn": "🟡",
        "Bảo trì": "🔴"
    }

    return icons.get(status, "⚪")


def change_room_status(room, status):

    index = st.session_state.rooms.index[
        st.session_state.rooms["Phòng"] == room
    ]

    if len(index) > 0:

        st.session_state.rooms.loc[
            index[0],
            "Trạng thái"
        ] = status


def new_booking_id():

    return f"BK{len(st.session_state.bookings) + 1:04d}"


# ============================================================
# 6. SIDEBAR
# ============================================================

with st.sidebar:

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            use_container_width=True
        )

    st.markdown(
        """
        <div class="hotel-title">
            CHARM PEARL HOTEL
        </div>

        <div class="hotel-subtitle">
            HOTEL MANAGEMENT SYSTEM
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    menu = st.radio(
        "QUẢN LÝ KHÁCH SẠN",

        [
            "🏠 Tổng quan",
            "🛏️ Quản lý phòng",
            "📅 Đặt phòng",
            "🛎️ Check-in",
            "🚪 Check-out",
            "👥 Khách hàng",
            "🍽️ Dịch vụ",
            "🧾 Hóa đơn",
            "💰 Doanh thu",
            "📊 Báo cáo"
        ]
    )

    st.divider()

    st.caption("SYSTEM STATUS")

    st.markdown(
        "🟢 **Hệ thống đang hoạt động**"
    )

    st.caption(
        "Charm Pearl Hotel · Vũng Tàu"
    )


# ============================================================
# 7. TRANG TỔNG QUAN
# ============================================================

if menu == "🏠 Tổng quan":

    st.markdown(
        f"""
        <div class="hero">

            <div>

                <div class="hero-tag">
                    WELCOME TO CHARM PEARL HOTEL
                </div>

                <h1>
                    Quản lý khách sạn
                    <br>
                    theo cách chuyên nghiệp.
                </h1>

                <p>
                    Vận hành phòng · Khách lưu trú · Dịch vụ · Doanh thu
                </p>

                <p style="font-size:12px">
                    Ngày hệ thống:
                    {date.today().strftime("%d/%m/%Y")}
                </p>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    rooms = st.session_state.rooms

    total_rooms = len(rooms)

    empty_rooms = len(
        rooms[rooms["Trạng thái"] == "Trống"]
    )

    occupied_rooms = len(
        rooms[rooms["Trạng thái"] == "Đang ở"]
    )

    reserved_rooms = len(
        rooms[rooms["Trạng thái"] == "Đã đặt"]
    )

    cleaning_rooms = len(
        rooms[rooms["Trạng thái"] == "Đang dọn"]
    )

    revenue = st.session_state.bookings[
        "Tổng tiền"
    ].sum()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "🏨 Tổng phòng",
        total_rooms
    )

    c2.metric(
        "🟢 Phòng trống",
        empty_rooms
    )

    c3.metric(
        "🔵 Đang ở",
        occupied_rooms
    )

    c4.metric(
        "🟣 Đã đặt",
        reserved_rooms
    )

    c5.metric(
        "💰 Doanh thu",
        money(revenue)
    )

    st.markdown(
        '<div class="section-title">🛏️ Sơ đồ 50 phòng</div>',
        unsafe_allow_html=True
    )

    floor_filter = st.selectbox(
        "Chọn tầng",
        ["Tất cả", 1, 2, 3, 4, 5]
    )

    if floor_filter == "Tất cả":

        display_rooms = rooms

    else:

        display_rooms = rooms[
            rooms["Tầng"] == floor_filter
        ]

    columns = st.columns(10)

    for i, (_, room) in enumerate(
        display_rooms.iterrows()
    ):

        with columns[i % 10]:

            st.markdown(
                f"""
                <div class="room-card">

                    <div class="room-number">
                        {room["Phòng"]}
                    </div>

                    <div class="room-type">
                        {room["Loại phòng"]}
                    </div>

                    <div class="room-status">
                        {status_icon(room["Trạng thái"])}
                        {room["Trạng thái"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.caption(
        f"""
        🟢 Trống: {empty_rooms}
        · 🔵 Đang ở: {occupied_rooms}
        · 🟣 Đã đặt: {reserved_rooms}
        · 🟡 Đang dọn: {cleaning_rooms}
        """
    )

    st.markdown(
        '<div class="section-title">📊 Tổng quan vận hành</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        occupancy = (
            occupied_rooms / total_rooms
            if total_rooms > 0
            else 0
        )

        st.markdown(
            '<div class="custom-card">',
            unsafe_allow_html=True
        )

        st.subheader("Công suất phòng")

        st.metric(
            "Tỷ lệ đang sử dụng",
            f"{occupancy:.0%}"
        )

        st.progress(occupancy)

        st.markdown(
            f"""
            <span class="small-text">
                {occupied_rooms}/{total_rooms}
                phòng đang có khách.
            </span>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader("Phân bổ trạng thái")

        st.bar_chart(
            rooms["Trạng thái"].value_counts()
        )

    with right:

        st.markdown(
            """
            <div class="custom-card">

                <h3>
                    ✨ Charm Pearl Hotel
                </h3>

                <p class="small-text">
                    Hệ thống quản lý khách sạn mô phỏng
                    với quy mô 50 phòng tại Vũng Tàu.
                </p>

                <hr>

                <b>🛏️ Room Management</b>

                <p class="small-text">
                    Theo dõi trạng thái phòng,
                    loại phòng và giá phòng.
                </p>

                <b>📅 Reservation</b>

                <p class="small-text">
                    Tiếp nhận và quản lý đặt phòng.
                </p>

                <b>🛎️ Front Office</b>

                <p class="small-text">
                    Check-in và check-out khách.
                </p>

                <b>💰 Revenue</b>

                <p class="small-text">
                    Theo dõi doanh thu phòng
                    và dịch vụ.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 8. QUẢN LÝ PHÒNG
# ============================================================

elif menu == "🛏️ Quản lý phòng":

    st.title("🛏️ Quản lý phòng")

    st.caption(
        "50 phòng · 5 tầng · 4 loại phòng"
    )

    rooms = st.session_state.rooms

    c1, c2, c3 = st.columns(3)

    with c1:

        floor = st.selectbox(
            "Tầng",
            ["Tất cả", 1, 2, 3, 4, 5],
            key="room_floor"
        )

    with c2:

        room_type = st.selectbox(
            "Loại phòng",
            ["Tất cả"] + list(ROOM_PRICES.keys()),
            key="room_type"
        )

    with c3:

        status = st.selectbox(
            "Trạng thái",
            ["Tất cả"] + ROOM_STATUS,
            key="room_status"
        )

    filtered = rooms.copy()

    if floor != "Tất cả":

        filtered = filtered[
            filtered["Tầng"] == floor
        ]

    if room_type != "Tất cả":

        filtered = filtered[
            filtered["Loại phòng"] == room_type
        ]

    if status != "Tất cả":

        filtered = filtered[
            filtered["Trạng thái"] == status
        ]

    columns = st.columns(5)

    for i, (_, room) in enumerate(
        filtered.iterrows()
    ):

        with columns[i % 5]:

            st.markdown(
                f"""
                <div class="custom-card">

                    <div style="
                        font-size:27px;
                        font-weight:800;
                        color:#082d4c;
                    ">
                        {room["Phòng"]}
                    </div>

                    <div class="small-text">
                        {room["Loại phòng"]}
                    </div>

                    <div class="price">
                        {money(room["Giá/đêm"])}
                    </div>

                    <br>

                    <b>
                        {status_icon(room["Trạng thái"])}
                        {room["Trạng thái"]}
                    </b>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader(
        "🔧 Cập nhật trạng thái phòng"
    )

    with st.form("change_status"):

        room = st.selectbox(
            "Chọn phòng",
            rooms["Phòng"].tolist()
        )

        new_status = st.selectbox(
            "Trạng thái mới",
            ROOM_STATUS
        )

        submit = st.form_submit_button(
            "CẬP NHẬT PHÒNG",
            use_container_width=True
        )

    if submit:

        change_room_status(
            room,
            new_status
        )

        st.success(
            f"Đã cập nhật phòng {room}: {new_status}"
        )

        st.rerun()


# ============================================================
# 9. ĐẶT PHÒNG
# ============================================================

elif menu == "📅 Đặt phòng":

    st.title("📅 Đặt phòng")

    st.caption(
        "Tạo và quản lý booking khách lưu trú"
    )

    available = st.session_state.rooms[
        st.session_state.rooms["Trạng thái"] == "Trống"
    ]

    if available.empty:

        st.warning(
            "Hiện tại không còn phòng trống."
        )

    else:

        with st.form("booking_form"):

            left, right = st.columns(2)

            with left:

                guest_name = st.text_input(
                    "Họ và tên khách *"
                )

                phone = st.text_input(
                    "Số điện thoại *"
                )

                room = st.selectbox(
                    "Phòng *",
                    available["Phòng"].tolist()
                )

            with right:

                checkin = st.date_input(
                    "Ngày nhận",
                    date.today() + timedelta(days=1)
                )

                checkout = st.date_input(
                    "Ngày trả",
                    date.today() + timedelta(days=2)
                )

                note = st.text_area(
                    "Ghi chú"
                )

            submit = st.form_submit_button(
                "📅 XÁC NHẬN ĐẶT PHÒNG",
                use_container_width=True
            )

        if submit:

            if not guest_name.strip():

                st.error(
                    "Vui lòng nhập họ tên khách."
                )

            elif not phone.strip():

                st.error(
                    "Vui lòng nhập số điện thoại."
                )

            elif checkout <= checkin:

                st.error(
                    "Ngày trả phải sau ngày nhận."
                )

            else:

                nights = (
                    checkout - checkin
                ).days

                room_price = int(
                    st.session_state.rooms.loc[
                        st.session_state.rooms["Phòng"]
                        == room,
                        "Giá/đêm"
                    ].iloc[0]
                )

                room_total = nights * room_price

                new_booking = pd.DataFrame(
                    [
                        [
                            new_booking_id(),
                            room,
                            guest_name.strip(),
                            phone.strip(),
                            checkin,
                            checkout,
                            nights,
                            room_total,
                            0,
                            room_total,
                            "Đã đặt"
                        ]
                    ],
                    columns=
                    st.session_state.bookings.columns
                )

                st.session_state.bookings = pd.concat(
                    [
                        st.session_state.bookings,
                        new_booking
                    ],
                    ignore_index=True
                )

                change_room_status(
                    room,
                    "Đã đặt"
                )

                st.success(
                    f"Đặt phòng {room} thành công."
                )

                st.metric(
                    "Tổng tiền dự kiến",
                    money(room_total)
                )


# ============================================================
# 10. CHECK-IN
# ============================================================

elif menu == "🛎️ Check-in":

    st.title("🛎️ Check-in")

    st.caption(
        "Tiếp nhận khách đến lưu trú"
    )

    available = st.session_state.rooms[
        st.session_state.rooms["Trạng thái"].isin(
            ["Trống", "Đã đặt"]
        )
    ]

    if available.empty:

        st.warning(
            "Không có phòng có thể check-in."
        )

    else:

        with st.form("checkin_form"):

            left, right = st.columns(2)

            with left:

                room = st.selectbox(
                    "Phòng",
                    available["Phòng"].tolist()
                )

                guest = st.text_input(
                    "Họ và tên khách"
                )

                phone = st.text_input(
                    "Số điện thoại"
                )

            with right:

                checkin = st.date_input(
                    "Ngày nhận",
                    date.today()
                )

                checkout = st.date_input(
                    "Ngày trả",
                    date.today() + timedelta(days=1)
                )

                initial_service = st.number_input(
                    "Dịch vụ ban đầu",
                    min_value=0,
                    max_value=10000000,
                    value=0,
                    step=50000
                )

            submit = st.form_submit_button(
                "🛎️ XÁC NHẬN CHECK-IN",
                use_container_width=True
            )

        if submit:

            if not guest.strip():

                st.error(
                    "Vui lòng nhập tên khách."
                )

            elif checkout <= checkin:

                st.error(
                    "Ngày trả phải sau ngày nhận."
                )

            else:

                nights = (
                    checkout - checkin
                ).days

                room_price = int(
                    st.session_state.rooms.loc[
                        st.session_state.rooms["Phòng"]
                        == room,
                        "Giá/đêm"
                    ].iloc[0]
                )

                room_total = (
                    nights * room_price
                )

                total = (
                    room_total
                    + initial_service
                )

                new_booking = pd.DataFrame(
                    [
                        [
                            new_booking_id(),
                            room,
                            guest.strip(),
                            phone.strip(),
                            checkin,
                            checkout,
                            nights,
                            room_total,
                            initial_service,
                            total,
                            "Đang ở"
                        ]
                    ],
                    columns=
                    st.session_state.bookings.columns
                )

                st.session_state.bookings = pd.concat(
                    [
                        st.session_state.bookings,
                        new_booking
                    ],
                    ignore_index=True
                )

                change_room_status(
                    room,
                    "Đang ở"
                )

                st.success(
                    f"Check-in phòng {room} thành công."
                )

                st.metric(
                    "Tạm tính",
                    money(total)
                )


# ============================================================
# 11. CHECK-OUT
# ============================================================

elif menu == "🚪 Check-out":

    st.title("🚪 Check-out")

    st.caption(
        "Thanh toán và hoàn tất lưu trú"
    )

    current = st.session_state.bookings[
        st.session_state.bookings["Trạng thái"]
        == "Đang ở"
    ]

    if current.empty:

        st.info(
            "Hiện không có khách đang lưu trú."
        )

    else:

        room = st.selectbox(
            "Chọn phòng",
            current["Phòng"].tolist()
        )

        index = current.index[
            current["Phòng"] == room
        ][0]

        booking = st.session_state.bookings.loc[
            index
        ]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Khách",
            booking["Tên khách"]
        )

        c2.metric(
            "Số đêm",
            booking["Số đêm"]
        )

        c3.metric(
            "Tiền phòng",
            money(booking["Tiền phòng"])
        )

        service_cost = st.number_input(
            "Dịch vụ phát sinh",
            min_value=0,
            max_value=10000000,
            value=int(booking["Dịch vụ"]),
            step=50000
        )

        total = (
            int(booking["Tiền phòng"])
            + service_cost
        )

        st.metric(
            "TỔNG THANH TOÁN",
            money(total)
        )

        if st.button(
            "💳 THANH TOÁN & CHECK-OUT",
            use_container_width=True
        ):

            st.session_state.bookings.loc[
                index,
                "Dịch vụ"
            ] = service_cost

            st.session_state.bookings.loc[
                index,
                "Tổng tiền"
            ] = total

            st.session_state.bookings.loc[
                index,
                "Trạng thái"
            ] = "Đã trả phòng"

            change_room_status(
                room,
                "Đang dọn"
            )

            st.success(
                f"Đã check-out phòng {room}."
            )

            st.rerun()


# ============================================================
# 12. KHÁCH HÀNG
# ============================================================

elif menu == "👥 Khách hàng":

    st.title("👥 Khách hàng")

    search = st.text_input(
        "🔎 Tìm theo tên, phòng hoặc số điện thoại"
    )

    data = st.session_state.bookings.copy()

    if search:

        mask = data.astype(str).apply(
            lambda column:
            column.str.contains(
                search,
                case=False,
                na=False
            )
        ).any(axis=1)

        data = data[mask]

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "📌 Khách đang lưu trú"
    )

    current = st.session_state.bookings[
        st.session_state.bookings["Trạng thái"]
        == "Đang ở"
    ]

    if current.empty:

        st.info(
            "Không có khách đang lưu trú."
        )

    else:

        st.dataframe(
            current[
                [
                    "Phòng",
                    "Tên khách",
                    "Số điện thoại",
                    "Ngày nhận",
                    "Ngày trả"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 13. DỊCH VỤ
# ============================================================

elif menu == "🍽️ Dịch vụ":

    st.title("🍽️ Dịch vụ khách sạn")

    st.caption(
        "Quản lý dịch vụ và bảng giá"
    )

    display = st.session_state.services.copy()

    display["Đơn giá"] = display[
        "Đơn giá"
    ].apply(money)

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "➕ Thêm dịch vụ"
    )

    with st.form("service_form"):

        c1, c2, c3 = st.columns(3)

        with c1:

            code = st.text_input(
                "Mã dịch vụ"
            )

        with c2:

            name = st.text_input(
                "Tên dịch vụ"
            )

        with c3:

            price = st.number_input(
                "Đơn giá",
                min_value=0,
                max_value=10000000,
                value=0,
                step=10000
            )

        submit = st.form_submit_button(
            "➕ THÊM DỊCH VỤ",
            use_container_width=True
        )

    if submit:

        if not code.strip() or not name.strip():

            st.error(
                "Vui lòng nhập đủ thông tin."
            )

        else:

            new_service = pd.DataFrame(
                [
                    [
                        code.upper(),
                        name.strip(),
                        price
                    ]
                ],
                columns=
                st.session_state.services.columns
            )

            st.session_state.services = pd.concat(
                [
                    st.session_state.services,
                    new_service
                ],
                ignore_index=True
            )

            st.success(
                "Đã thêm dịch vụ."
            )

            st.rerun()


# ============================================================
# 14. HÓA ĐƠN
# ============================================================

elif menu == "🧾 Hóa đơn":

    st.title("🧾 Hóa đơn")

    data = st.session_state.bookings.copy()

    if data.empty:

        st.info(
            "Chưa có dữ liệu hóa đơn."
        )

    else:

        display = data.copy()

        display["Tiền phòng"] = display[
            "Tiền phòng"
        ].apply(money)

        display["Dịch vụ"] = display[
            "Dịch vụ"
        ].apply(money)

        display["Tổng tiền"] = display[
            "Tổng tiền"
        ].apply(money)

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        booking_id = st.selectbox(
            "Chọn mã booking",
            data["Mã đặt phòng"].tolist()
        )

        invoice = data[
            data["Mã đặt phòng"] == booking_id
        ].iloc[0]

        st.markdown(
            f"""
            <div class="custom-card">

                <h2>
                    CHARM PEARL HOTEL
                </h2>

                <p class="small-text">
                    PHIẾU THANH TOÁN
                </p>

                <hr>

                <b>Mã booking:</b>
                {invoice["Mã đặt phòng"]}

                <br>

                <b>Khách:</b>
                {invoice["Tên khách"]}

                <br>

                <b>Phòng:</b>
                {invoice["Phòng"]}

                <br>

                <b>Ngày nhận:</b>
                {invoice["Ngày nhận"]}

                <br>

                <b>Ngày trả:</b>
                {invoice["Ngày trả"]}

                <hr>

                <b>Tiền phòng:</b>
                {money(invoice["Tiền phòng"])}

                <br>

                <b>Dịch vụ:</b>
                {money(invoice["Dịch vụ"])}

                <h2>
                    TỔNG:
                    {money(invoice["Tổng tiền"])}
                </h2>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 15. DOANH THU
# ============================================================

elif menu == "💰 Doanh thu":

    st.title("💰 Doanh thu")

    data = st.session_state.bookings

    room_revenue = data[
        "Tiền phòng"
    ].sum()

    service_revenue = data[
        "Dịch vụ"
    ].sum()

    total_revenue = data[
        "Tổng tiền"
    ].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🏨 Tiền phòng",
        money(room_revenue)
    )

    c2.metric(
        "🍽️ Dịch vụ",
        money(service_revenue)
    )

    c3.metric(
        "💰 Tổng doanh thu",
        money(total_revenue)
    )

    st.divider()

    revenue_chart = pd.DataFrame(
        {
            "Khoản thu": [
                "Tiền phòng",
                "Dịch vụ"
            ],

            "Doanh thu": [
                room_revenue,
                service_revenue
            ]
        }
    )

    st.subheader(
        "📊 Cơ cấu doanh thu"
    )

    st.bar_chart(
        revenue_chart.set_index(
            "Khoản thu"
        )
    )

    st.subheader(
        "Danh sách giao dịch"
    )

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 16. BÁO CÁO
# ============================================================

elif menu == "📊 Báo cáo":

    st.title("📊 Báo cáo quản trị")

    rooms = st.session_state.rooms

    bookings = st.session_state.bookings

    left, right = st.columns(2)

    with left:

        st.subheader(
            "Cơ cấu loại phòng"
        )

        st.bar_chart(
            rooms["Loại phòng"].value_counts()
        )

    with right:

        st.subheader(
            "Trạng thái phòng"
        )

        st.bar_chart(
            rooms["Trạng thái"].value_counts()
        )

    st.divider()

    total_rooms = len(rooms)

    occupied = len(
        rooms[
            rooms["Trạng thái"] == "Đang ở"
        ]
    )

    occupancy = (
        occupied / total_rooms
        if total_rooms
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Tổng phòng",
        total_rooms
    )

    c2.metric(
        "Đang ở",
        occupied
    )

    c3.metric(
        "Công suất",
        f"{occupancy:.0%}"
    )

    c4.metric(
        "Booking",
        len(bookings)
    )

    st.subheader(
        "🛏️ Báo cáo phòng"
    )

    room_report = rooms.copy()

    room_report["Giá/đêm"] = room_report[
        "Giá/đêm"
    ].apply(money)

    st.dataframe(
        room_report,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "📅 Báo cáo booking"
    )

    st.dataframe(
        bookings,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <hr>

    <div style="
        text-align:center;
        color:#71808e;
        font-size:12px;
        padding:10px;
    ">

        CHARM PEARL HOTEL · VŨNG TÀU
        <br>
        Hotel Management System · Streamlit

    </div>
    """,
    unsafe_allow_html=True
)
