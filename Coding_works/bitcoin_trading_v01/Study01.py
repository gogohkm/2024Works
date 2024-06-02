# git을 공부하기 위해 작성
# 지금 git token을 mac에서 어떻게 저장하는지 이해하려고 함.
# git token을 저장하는 방법을 알아보자.


# git token을 저장하는 방법
# 1. git token을 생성한다.
# 2. git token을 저장한다.

# git token을 생성하는 방법
# 1. github.com에 접속한다.
# 2. 로그인한다.
# 3. 오른쪽 상단의 프로필 사진을 클릭한다.
# 4. Settings를 클릭한다.
# 5. Developer settings를 클릭한다.
# 6. Personal access tokens를 클릭한다.
# 7. Generate new token을 클릭한다.
# 8. note에 저장할 token의 이름을 입력한다.
# 9. expiration을 선택한다.
# 10. repo를 선택한다.
# 11. Generate token을 클릭한다.
# 12. token을 복사한다.

# git token을 저장하는 방법
# 1. terminal을 실행한다.
# 2. git config --global credential.helper store를 입력한다.
# 3. git push를 입력한다.
# 4. username과 password를 입력한다.
# 5. 다음부터는 username과 password를 입력하지 않아도 된다.
