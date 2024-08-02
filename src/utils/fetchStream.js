async function fetchStream(url, data, onDataChunk, onError, onFinally) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const reader = response.body.getReader();
        let done = false;
        while (!done) {
            const { value, done: newDone } = await reader.read();
            done = newDone;
            if (!done) {
                const chunk = new TextDecoder("utf-8").decode(value);
                onDataChunk(chunk); // 调用回调函数处理数据块
            }
        }
    } catch (error) {
        if (onError) onError(error); // 调用错误处理回调函数
    } finally {
        if (onFinally) onFinally(); // 调用最终回调函数
    }
}

export default fetchStream;