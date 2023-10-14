import datetime
import os
import pytest
import requests
from py.xml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_mainpy_directory_path():
    # 获取当前脚本文件的绝对路径
    current_script_path = os.path.abspath(__file__)
    # 获取当前脚本文件所在目录的路径
    script_directory = os.path.dirname(current_script_path)
    # 获取 main.py 同一层目录的路径
    parent_directory = os.path.dirname(script_directory)
    return os.path.dirname(parent_directory)


# 設置HTML报告的存储路径(...\TestReport_年-月-日.html)
def pytest_configure(config):
    # 定义报告的存档路径
    report_path = f'{get_mainpy_directory_path()}\\_testreport\\TestReport_{str(datetime.date.today())}.html'
    # 使用 config.option.htmlpath 来设置报告路径
    config.option.htmlpath = report_path


def pytest_html_report_title(report):
    report.title = "Pytest測試報告"  # 設置HTML報告的標題


def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)  # 從Environment中删除JAVA_HOME項目
    metadata['测试项目'] = "檢查URL"
    metadata['sitemap網址'] = "https://www.esunbank.com/bank/sitemap.xml"


def pytest_html_results_summary(prefix, summary, postfix):
    # prefix.clear() # 清空summary中的内容
    prefix.extend([f"檢查URL狀態, 可訪問, 網頁導轉至其他頁, 不可訪問...等"])  # 设設置HTML報告的摘要信息


# 設置report的測試結果欄位名
def pytest_html_results_table_header(cells):
    cells.clear()
    cells.insert(0, html.th('Result', class_='sortable', col='result'))
    cells.insert(1, html.th('Test Case', class_='sortable', col='test_case'))
    cells.insert(2, html.th('Duration', class_='sortable time', col='duration'))
    cells.insert(3, html.th('Notes'))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    # 这一行获取了 pytest-html 插件的实例，以便后续将截图添加到报告中。
    pytest_html = item.config.pluginmanager.getplugin('html')
    # 这一行表示将控制权传递给测试执行的结果，后续代码将在测试执行完成后继续执行。
    outcome = yield
    # 这一行获取了测试报告的结果，包括测试的状态和其他信息。
    report = outcome.get_result()
    # 这一行获取报告中的额外信息（extra），如果没有额外信息，就创建一个空列表。
    extra = getattr(report, 'extra', [])
    # 这一行检查报告的执行阶段，只有在测试用例执行完毕后（'call'）或在设置阶段（'setup'）时才会继续执行以下代码。
    if report.when == 'call' or report.when == "setup":
        # 这一行调用 _capture_screenshot() 函数来捕获屏幕截图，并将截图数据保存在 screen_img 变量中。
        screen_img = _capture_screenshot()
        # 这一行创建一个包含截图的 HTML 元素，其中包括一个 <img> 标签来显示截图，点击截图时可以在新窗口中查看。%s 会被替换为实际的截图数据。
        html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:640px;height:360px;" ' \
               'οnclick="window.open(this.src)" align="right"/></div>' % screen_img
        # 这一行将包含截图的 HTML 元素添加到报告的额外信息中，以便在报告中显示截图。
        extra.append(pytest_html.extras.html(html))
    # 最后，这一行将更新后的额外信息重新赋值给报告，以确保嵌入的截图被添加到报告中。
    report.extras = extra


def _capture_screenshot():
    '''
    ** 作者：上海-悠悠 QQ交流群：313782132**
    截图保存为base64，展示到html中
    :return:
    '''
    return driver.get_screenshot_as_base64()

driver = None

@pytest.fixture(scope='session', autouse=True)
def browser(request):
    global driver
    # if driver is None:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # 设置浏览器参数
    chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.add_argument("--hide-scrollbars")
    driver = webdriver.Chrome(options=chrome_options)  # 创建一个chrome的webdrive
    # driver=webdriver.Chrome()

    def end():
        driver.quit()

    request.addfinalizer(end)
    return driver
