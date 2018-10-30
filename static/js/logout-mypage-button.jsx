function LogoutButton(props) {
    localStorage.removeItem('cachedId');
    return (
        <button type='button'>
            <a href="/log-out">Log out</a>
        </button>
    );
}

function MyPageButton(props) {
    return (
        <button type='button'>
            <a href={"/users/"}>My page</a>
        </button>
    );
}

function MyLoggedInButtons(props) {
    return(
    <div>
        <MyPageButton />
        <LogoutButton />
    </div>
        )
}

ReactDOM.render(
    <MyLoggedInButtons />, document.getElementById('root')
    )