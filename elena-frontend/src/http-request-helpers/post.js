import axios from 'axios';

// Universal fetch request using axios
export default function universalPost(
  setResponse,
  endpoint,
  onError,
  onSuccess,
  requestBody,
) {
  setResponse({
    data: null,
    loading: true,
    error: null,
  });

  axios
    .post(endpoint, requestBody, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Referrer-Policy': 'no-referrer'
      }
    })
    .then((resp) => {
      setResponse({
        data: resp.data,
        loading: false,
        error: null,
      });
      onSuccess && onSuccess(resp);
    })
    .catch((err) => {
      setResponse({
        data: null,
        loading: false,
        error: err,
      });
      onError && onError(err);
    });
}
